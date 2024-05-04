from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def detektirajKorisnika(user):
    if user.role == 1:
        redirectUrl = 'opg_nadzorna_ploca'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'kupac_nadzorna_ploca'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl


def posalji_verifikacijski_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Molimo Vas aktivirajte Vaš račun!'
    message = render_to_string('korisnicki_racuni/email/verifikacija_racuna_mailom.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    mail.send()
