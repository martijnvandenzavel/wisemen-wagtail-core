from allauth.account.adapter import DefaultAccountAdapter
from django_rq import get_queue
from environ import Env

from wisemen.email import send_templated_mail


class AccountAdapter(DefaultAccountAdapter):
    """
    Custom AccountAdapter to send emails asynchronously.
    Wire in `locale=<locale>` when calling the various routes,
    otherwise it defaults to the locale `en`.

    For now only used for email confirmation.
    @Todo: Add other emails to this adapter.
    """

    def send_mail(self, template_prefix, email, context):
        msg = self.render_mail(template_prefix, email, context)

        ENV = Env()  # noqa: N806
        queue = get_queue(ENV("REDIS_QUEUE"))

        locale = context["request"].GET.get("locale", "en")

        template_variables = {}
        if template_prefix == "account/email/email_confirmation_signup":
            template_variables = {"email": email, "key": context["key"]}
        elif template_prefix == "account/email/password_reset_key":
            url = context["password_reset_url"].split("/")
            template_variables = {
                "email": email,
                "uid": context["password_reset_url"].split("/")[-2],
                "token": context["password_reset_url"].split("/")[-1],
            }

        queue.enqueue(
            send_templated_mail,
            to_addresses=msg.to,
            subject=msg.subject,
            template_name=f"{template_prefix}_{locale}.html",
            template_variables=template_variables,
            tags=template_prefix.split("/")[1:],
        )
