import resend
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class ResendEmailBackend(BaseEmailBackend):

    def open(self):
        resend.api_key = settings.RESEND_API_KEY
        return True

    def close(self):
        pass

    def send_messages(self, email_messages):
        resend.api_key = settings.RESEND_API_KEY
        sent = 0
        for message in email_messages:
            try:
                resend.Emails.send({
                    'from': message.from_email or settings.DEFAULT_FROM_EMAIL,
                    'to': message.to,
                    'subject': message.subject,
                    'text': message.body,
                })
                sent += 1
            except Exception as e:
                if not self.fail_silently:
                    raise e
        return sent