from typing import Dict, List
import environ

from django.core.mail import EmailMessage
from django.template.loader import get_template

ENV = environ.Env()


def send_templated_mail(
    to_addresses: List[str],
    subject: str,
    template_name: str,
    template_variables: Dict,
    tags: List[str] = [],
    tracking: bool = True,
    track_clicks: bool = True,
    track_opens: bool = True,
):
    """
    Base email handler.
    Not making use of Django Anymail just yet as this gives us enough possibilities.

    Templates are stored in the various app directories and must be unique.

    Various headers are set for MailGun to allow tracking and tagging. 
    """

    headers = {}

    if tags:
        headers["X-Mailgun-Tag"] = ",".join(tags)

    if tracking:
        headers["X-Mailgun-Track"] = "yes"

    if track_clicks:
        headers["X-Mailgun-Track-Clicks"] = "yes"

    if track_opens:
        headers["X-Mailgun-Track-Opens"] = "yes"

    message = get_template(template_name).render(template_variables)

    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=ENV("EMAIL_FROM"),
        to=to_addresses,
        headers=headers,
    )
    mail.content_subtype = "html"

    return mail.send()
