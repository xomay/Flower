from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from flower_app.models.ParamsJE import ParamsJE

def send_mail(context, params_je, file_name, target):
    email_html_message = render_to_string(file_name + '.html', context)
    email_plaintext_message = render_to_string(file_name + '.txt', context)
    msg = EmailMultiAlternatives(
        # title:
        "[{je_name}] Création de compte {title} - Réalisateur".format(je_name=params_je.je_name, title="Flower"),
        # message:
        email_plaintext_message,
        # from:
        params_je.je_contact,
        # to:
        [target]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()

def send_mail_rea_account_creation(realisateur, username, password):
    params_je = ParamsJE.objects.get(pk=1)
    context = {
        'je_name': params_je.je_name,
        'realisateur': realisateur.firstname + " " + realisateur.lastname,
        'contact': params_je.je_contact,
        'username': username,
        'password': password,
        'connection_url': "{}/#/login".format(settings.FRONT_END)
    }
    send_mail(context, params_je, 'rea_account_create', realisateur.email_insa)

def send_mail_rea_account_deletion(realisateur):
    params_je = ParamsJE.objects.get(pk=1)
    context = {
        'je_name': params_je.je_name,
        'realisateur': realisateur.firstname + " " + realisateur.lastname,
        'contact': params_je.je_contact,
    }
    send_mail(context, params_je, 'rea_account_delete', realisateur.email_insa)