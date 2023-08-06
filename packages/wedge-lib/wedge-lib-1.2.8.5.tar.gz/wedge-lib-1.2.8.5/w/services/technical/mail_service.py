import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from w.services.abstract_service import AbstractService


class EmailService(AbstractService):
    @staticmethod
    def render_template(template_name, context=None):
        """
        Render mail template
        """
        return render_to_string(template_name, context)

    @classmethod
    def send(cls, recipients, subject, message, attach_files=None, **options):
        """
        Send an email

        Args:
            recipients(str|list|dict): email or list of emails or dict
                {
                  "to": <email or list of emails>
                  "bcc": <email or list of emails>
                  "cc": <email or list of emails>
                }
            subject (str|dict): subject or template (as dict) :
                {"template_name": <str>, "context": <dict> }
            message (str|dict): message or template (as dict) :
                {"template_name": <str>, "context": <dict> }
            attach_files:  (dict) list of file to attach
                {"attach_files": [<str>], "context": <dict> }
            **options (dict):
                    'from_email': <from_email, default is settings.DEFAULT_FROM_EMAIL>,
                    'reply_to' : <reply to email, None by default>

        Returns:
            int: number of email sent
        """
        default_params = {
            "from_email": settings.DEFAULT_FROM_EMAIL,
            "to": None,
            "bcc": None,
            "cc": None,
            "connection": None,
            "attachments": None,
            "headers": None,
            "reply_to": settings.DEFAULT_REPLY_TO,
        }

        if not isinstance(recipients, dict):
            recipients = {"to": recipients}

        # noinspection PyDictCreation
        params = {**default_params, **recipients, **options}

        # convert str recipient to list
        for key in ["to", "bcc", "cc", "reply_to"]:
            if params[key] and not isinstance(params[key], list):
                params[key] = [params[key]]

        if isinstance(subject, dict):
            subject = render_to_string(**subject)

        is_html = False
        if isinstance(message, dict):
            _, ext = os.path.splitext(message["template_name"])
            is_html = ext == ".html"
            message = render_to_string(**message)

        params["subject"] = subject
        params["body"] = message
        email = EmailMessage(**params)

        if is_html:
            email.content_subtype = "html"

        if attach_files:
            for file in attach_files:
                email.attach_file(file)

        return email.send()
