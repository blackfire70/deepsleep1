from django.core import mail
from django.contrib.auth.models import User

from settings.base import get_key

def send_activation_mail(user):
    '''
        Sends an activation email to the user
        param user: User instance
        param token: AccessToken instance
    '''


    from_email = get_key('EMAIL_HOST_USER')
    body = '''
        Hi, thank you for signing up on our app.
        click {} activate your account
        Thanks. 
        The App Team.
    '''

    # The user's hash will be used as a token
    algo, salt, p_hash = user.password.split('$', 2)
    activation_url = (
        'http://localhost:8000/api/v1/user/activate/{}/?token={}'.format(
            user.id,
            p_hash
        )
    )
    plain_body = body.format(activation_url)
    html_body = body.format('<a href="{}">Here</a>'.format(activation_url))
    email = mail.EmailMultiAlternatives(
        'Account Activation',
        plain_body,
        from_email,
        [user.email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send()
