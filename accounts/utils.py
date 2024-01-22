from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
#forbiding customer to access the vendor dashboard
def check_role_vendor(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    
#forbiding vendor to access the customer dashboard
def check_role_customer(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
def send_verification_email(request, user, mail_subject, email_template):
    current_site = get_current_site(request)
    from_email = settings.DEFAULT_FROM_EMAIL
    context = {
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
    }
    message = render_to_string(email_template, context)
    mail = EmailMessage(mail_subject, message, from_email, to=[user.email])
    mail.send()


   # 'emails/reset_password_validate.html'
    
def send_notification(mail_subject, email_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(email_template, context)
    user = context['user']
    mail = EmailMessage(mail_subject, message, from_email, to=[user.email])
    mail.send()