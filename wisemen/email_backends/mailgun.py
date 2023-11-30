import logging

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address
from environ import Env
from requests import post


logger = logging.getLogger(__name__)


class MailGunBackend(BaseEmailBackend):
    def __init__(self, api_path=None, api_key=None, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        ENV = Env()

        self.api_path = api_path or ENV("MAILGUN_API_PATH")
        self.api_key = api_key or ENV("MAILGUN_API_KEY")

    def send_messages(self, email_messages):
        if not email_messages:
            return

        msg_count = 0
        last_exception = None

        for message in email_messages:
            sent = self._send(message)
            if sent.status_code == 200:
                msg_count += 1

        if not self.fail_silently and last_exception:
            raise last_exception

        return msg_count

    def _send(self, email_message):
        return post(
            f"{self.api_path}/messages",
            auth=("api", self.api_key),
            data={
                "from": sanitize_address(
                    email_message.from_email, email_message.encoding
                ),
                "message-headers": email_message.extra_headers,
                "to": [
                    sanitize_address(addr, email_message.encoding)
                    for addr in email_message.recipients()
                ],
                "subject": email_message.subject,
                "html": email_message.body,
            },
        )
