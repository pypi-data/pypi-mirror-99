import requests
from django.conf import settings
from dnoticias_services.mail.base import BaseMail


class SendEmail(BaseMail):
    def __call__(self, email, template_uuid, brand_group_uuid, subject, context=dict(), from_email=None, from_name=None, attachments=[], track_opens=True, track_clicks=True, api_key=None):
        url = settings.SEND_EMAIL_API_URL
        _api_key = api_key or self.api_key
        
        response = requests.post(
            url,
            headers={
                "Authorization" : "Api-Key {}".format(_api_key)
            },
            json={
                "email" : email,
                "template_uuid" : template_uuid,
                "brand_group_uuid" : brand_group_uuid,
                "subject" : subject,
                "context" : context,
                "from_email" : from_email,
                "from_name" : from_name,
                "attachments" : attachments,
                "track_opens" : track_opens,
                "track_clicks" : track_clicks,
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        return response

send_email = SendEmail()

class SendEmailBulk(BaseMail):
    def __call__(self, emails=[], template_uuid=None, brand_group_uuid=None, subject="", context=list(), from_email=None, from_name=None, attachments=[], track_opens=True, track_clicks=True, api_key=None):
        url = settings.SEND_EMAIL_BULK_API_URL
        _api_key = api_key or self.api_key
        
        response = requests.post(
            url,
            headers={
                "Authorization" : "Api-Key {}".format(_api_key)
            },
            json={
                "emails" : emails,
                "template_uuid" : template_uuid,
                "brand_group_uuid" : brand_group_uuid,
                "subject" : subject,
                "context" : context,
                "from_email" : from_email,
                "from_name" : from_name,
                "attachments" : attachments,
                "track_opens" : track_opens,
                "track_clicks" : track_clicks,
            },
            timeout=self.timeout
        )
        response.raise_for_status()
        return response

send_email_bulk = SendEmailBulk()

__all__ = ("send_email", "send_email_bulk")
