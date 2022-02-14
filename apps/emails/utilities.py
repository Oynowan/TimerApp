#
# Import Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# function


def send_invitation_email(to_email, code):

    from_email = settings.DEFAULT_FROM_EMAIL
    acceptation_url = settings.ACCEPTATION_URL + code
    subject = 'Invitation to BV-Timer'
    text_content = f'Invitation To BV-Timer. Your registration link: {acceptation_url}'
    html_content = render_to_string('emails/email_invitation.html', {'code': code, 'acceptation_url': acceptation_url})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def reset_password_email(to_email, code):
    from_email = settings.DEFAULT_FROM_EMAIL
    acceptation_url = settings.RESET_PASSWORD_URL + code
    subject = 'Reset Password - BV-Timer'
    text_content = f'Reset password to your BV-Timer account. Link: {acceptation_url}. Link is active for 15minutes.'
    html_content = render_to_string('emails/email_reset_password.html', {'code': code, 'acceptation_url': acceptation_url})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def password_manager_email(to_email, acc):
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = 'BV-Timer Password Manager Request'
    text_content = f'Password Manager Request for Website {acc.website_name} - Username {acc.username} - Password {acc.get_password()}'
    html_content = render_to_string('emails/email_password_manager.html', {'website':acc.website_name, 'username': acc.username, 'password': acc.get_password()})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()