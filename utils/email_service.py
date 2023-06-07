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
    


def password_reset_otp_email(email, otp):

    try:
        email_subject = 'Password Reset OTP'
        SYSTEM_EMAIL = settings.EMAIL_HOST_USER
        to = email
        message = f'Dear Admin, use otp {otp} to complete your request to change password.' 

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
    
def password_resend_reset_otp_email(email, otp):

    try:
        email_subject = 'Password Resend Reset OTP'
        SYSTEM_EMAIL = settings.EMAIL_HOST_USER
        to = email
        message = f'Dear Admin, you requested for a resend of otp, use otp {otp} to complete your request to change password.' 

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
    
def admin_department_otp_activate(email, otp, department_name):

    try:
        email_subject = 'Department Activation OTP'
        SYSTEM_EMAIL = settings.EMAIL_HOST_USER
        to = email
        message = f'Dear Admin, you iniatited a creation of department {department_name}, use otp {otp} to complete your request to activate password.' 

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
    