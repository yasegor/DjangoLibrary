from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.views import View


def send_mail_to_verify(request, user):
    current_site = get_current_site(request)
    message = render_to_string("auth/verify_email.html", {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    mail_subject = 'Email verification from Django Library'
    email = EmailMessage(mail_subject, message, to=[user.email])
    if email.send():
        messages.success(request, f'''Dear <b>{user}</b>, please go to you email <b>{user.email}</b> inbox and click on
                received activation link to confirm and complete the registration.<br>
                <b>Note:</b> Check your spam folder.
                ''')
    else:
        messages.error(request, f'Problem sending email to {user.email}, check if you typed it correctly.')


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.profile.verified = True
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, "Thank you for your email confirmation!")
            return redirect('index')
        messages.error(request, 'Your link is incorrect!')
        return redirect('index')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user
