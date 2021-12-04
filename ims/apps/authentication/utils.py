from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

import uuid
def unique_upload(instance, filename):
    ext = filename.split('.').pop()
    return "{}.{}".format(uuid.uuid4(), ext)


def send_email(context, html_template, txt_template, title=None, user_email=None):

    # render email text
    email_html_message = render_to_string(html_template, context)
    email_plain_text_message = render_to_string(txt_template, context)

    msg = EmailMultiAlternatives(
        # title:
        title,
        # message:
        email_plain_text_message,
        # from:
        settings.DEFAULT_FROM_EMAIL,
        # to:
        [user_email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()