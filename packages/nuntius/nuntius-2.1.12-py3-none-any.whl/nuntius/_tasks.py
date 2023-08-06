"""
    Nuntius needs its own celery app. This module is named _tasks so it is not autodiscovered by other celery app that
    live in the project.
"""

import re
from itertools import count
from smtplib import SMTPServerDisconnected, SMTPRecipientsRefused
from time import sleep
from urllib.parse import quote as url_quote

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template import Template, Context
from django.urls import reverse
from django.utils import timezone

from nuntius.celery import nuntius_celery_app
from nuntius.models import (
    Campaign,
    CampaignSentEvent,
    CampaignSentStatusType,
    AbstractSubscriber,
)
from nuntius.utils import sign_url, extend_query

try:
    from anymail.exceptions import AnymailRecipientsRefused
except:

    class AnymailRecipientsRefused(BaseException):
        pass


def replace_url(url, campaign, tracking_id, link_index, public_url):
    url = extend_query(
        url,
        defaults={
            "utm_content": link_index,
            "utm_term": getattr(campaign.segment, "utm_term", ""),
        },
    )

    return public_url + reverse(
        "nuntius_track_click",
        kwargs={
            "tracking_id": tracking_id,
            "signature": sign_url(campaign, url),
            "link": url_quote(url, safe=""),
        },
    )


def replace_vars(campaign, data, public_url):
    context = Context(data)

    html_rendered_content = Template(campaign.message_content_html).render(
        context=context
    )

    link_counter = count()
    html_rendered_content = re.sub(
        r"(<a[^>]* href\s*=[\s\"']*)(http[^\"'>\s]+)",
        lambda match: match.group(1)
        + replace_url(
            url=match.group(2),
            campaign=campaign,
            tracking_id=data["nuntius_tracking_id"],
            link_index=f"link-{next(link_counter)}",
            public_url=public_url,
        ),
        html_rendered_content,
        flags=re.MULTILINE | re.IGNORECASE,
    )

    text_rendered_content = Template(campaign.message_content_text).render(
        context=context
    )

    return text_rendered_content, html_rendered_content


def reset_connection(connection):
    try:
        connection.close()
    except Exception:
        pass

    for retry in reversed(range(1, 11)):
        try:
            sleep(1 / retry)
            connection.open()
        except Exception:
            connection.close()
        else:
            break


def insert_tracking_image(public_url, html_message):
    img_url = (
        public_url + reverse("nuntius_mount_path") + "open/{{ nuntius_tracking_id }}"
    )
    img = '<img src="{}" width="1" height="1" alt="nt">'.format(img_url)
    return re.sub(
        r"(<\/body\b)", img + r"\1", html_message, flags=re.MULTILINE | re.IGNORECASE
    )


@nuntius_celery_app.task()
def send_campaign(campaign_pk, public_url):
    campaign = Campaign.objects.get(pk=campaign_pk)
    campaign.status = Campaign.STATUS_SENDING
    if campaign.first_sent is None:
        campaign.first_sent = timezone.now()
    campaign.save(update_fields=["status", "first_sent"])

    if campaign.segment is None:
        model = settings.NUNTIUS_SUBSCRIBER_MODEL
        model_class = ContentType.objects.get(
            app_label=model.split(".")[0], model=model.split(".")[1].lower()
        ).model_class()
        queryset = model_class.objects.all()
    else:
        queryset = campaign.segment.get_subscribers_queryset()

    campaign.message_content_html = insert_tracking_image(
        public_url, campaign.message_content_html
    )

    def send_message(connection, sent_event, message, retries=10):
        try:
            message.send()
        except SMTPServerDisconnected as e:
            if retries == 0:
                campaign.status = Campaign.STATUS_ERROR
                campaign.save(update_fields=["status"])
                raise e

            reset_connection(connection)

            sleep(1 / retries)

            send_message(connection, sent_event, message, retries=retries - 1)
        except (SMTPRecipientsRefused, AnymailRecipientsRefused):
            sent_event.result = CampaignSentStatusType.BLOCKED
            sent_event.save()
        else:
            if hasattr(message, "anymail_status"):
                if message.anymail_status.recipients[sent_event.email].status in [
                    "invalid",
                    "rejected",
                    "failed",
                ]:
                    sent_event.result = CampaignSentStatusType.REJECTED
                else:
                    sent_event.result = CampaignSentStatusType.UNKNOWN
                sent_event.esp_message_id = message.anymail_status.recipients[
                    sent_event.email
                ].message_id
            else:
                sent_event.result = CampaignSentStatusType.UNKNOWN
            sent_event.save()

    try:
        with mail.get_connection(
            backend=getattr(settings, "NUNTIUS_EMAIL_BACKEND", None)
        ) as connection:
            for subscriber in queryset.iterator():
                if (
                    subscriber.get_subscriber_status()
                    != AbstractSubscriber.STATUS_SUBSCRIBED
                ):
                    continue

                email = subscriber.get_subscriber_email()

                (sent_event, created) = CampaignSentEvent.objects.get_or_create(
                    campaign=campaign, subscriber=subscriber, email=email
                )

                if sent_event.result != CampaignSentStatusType.PENDING:
                    continue

                with transaction.atomic():
                    sent_event = CampaignSentEvent.objects.select_for_update().get(
                        subscriber=subscriber, campaign=campaign
                    )

                    if sent_event.result != CampaignSentStatusType.PENDING:
                        continue

                    subscriber_data = {
                        "nuntius_tracking_id": sent_event.tracking_id,
                        **subscriber.get_subscriber_data(),
                    }

                    from_email = (
                        f"{campaign.message_from_name} <{campaign.message_from_email}>"
                        if campaign.message_from_name
                        else campaign.message_from_email
                    )
                    text_body, html_body = replace_vars(
                        campaign, subscriber_data, public_url
                    )
                    message = EmailMultiAlternatives(
                        subject=campaign.message_subject,
                        body=text_body,
                        from_email=from_email,
                        to=[email],
                        reply_to=campaign.message_reply_to_email,
                        connection=connection,
                    )
                    message.attach_alternative(html_body, "text/html")
                    send_message(connection, sent_event, message)

            campaign.status = Campaign.STATUS_SENT
            campaign.task_uuid = None
            campaign.save(update_fields=["status", "task_uuid"])
    except Exception as e:
        campaign.status = Campaign.STATUS_ERROR
        campaign.task_uuid = None
        campaign.save(update_fields=["status", "task_uuid"])
        raise e
