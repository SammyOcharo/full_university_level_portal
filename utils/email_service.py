from rest_framework. response import Response
from rest_framework import status
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def login_otp_email(email, otp):

    try:
        email_subject = 'Login OTP'
        SYSTEM_EMAIL = settings.EMAIL_HOST_USER
        to = email
        message = f'Dear Admin, use otp {otp} to complete your request to sign in.' 

        html_context = render_to_string("index.html",
                                         {'title': email_subject,
                                          'message': message}
                                        )
        email_content = EmailMultiAlternatives(
            email_subject,
            html_context,
            SYSTEM_EMAIL,
            [to]
        )

        email_content.attach_alternative(html_context, "text/html")
        email_content.send()

        return True

    except Exception as e:
        print(str(e))
        return False