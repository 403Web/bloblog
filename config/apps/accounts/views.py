from django.views.generic.base import View
from django.views.generic import CreateView
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView as DefaultPasswordChangeView
)
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from mail_templated import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from .forms import SignUpForm


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{user.email}{user.is_verified}{timestamp}'


User = get_user_model()
email_verification_token = EmailVerificationTokenGenerator()


def send_email(request, user, template_name):
    token = email_verification_token.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    context = {
        'user': user,
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': request.get_host(),
        'uidb64': uidb64,
        'token': token
    }

    email = EmailMessage(
        template_name,
        context,
        settings.EMAIL_HOST_USER,
        to=[user.email]
    )
    email.send()


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'auth/registration/signup.html'
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        super().form_valid(form)

        login(self.request, self.object)
        send_email(
            self.request,
            self.object,
            'auth/registration/email_verification.html'
        )

        return render(self.request, 'auth/registration/email_sent.html')


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('core:index'))

        return super().get(request, *args, **kwargs)


class EmailVerificationView(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            pk = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=pk)
        except (ValueError, TypeError, OverflowError, User.DoesNotExist):
            user = None

        if (
            user is not None and
            (not_verified := not user.is_verified) and
            email_verification_token.check_token(user, token)
        ):
            user.is_verified = True
            user.save()
            return redirect(reverse_lazy('core:index')) # TODO: messages
        return redirect(reverse_lazy('core:index')) # TODO: messages


class ResendVerificationView(View):

    def post(self, request, *args, **kwargs):
        if (
            logged_in := request.user.is_authenticated and
            not request.user.is_verified
        ):
            send_email(
                request,
                request.user,
                'auth/registration/email_verification.html'
            )

            return render(request, 'auth/registration/email_sent.html')

        if logged_in:
            return redirect(reverse_lazy('core:index')) # TODO: messages

        return redirect(reverse_lazy('accounts:signin'))


class SignInView(LoginView):
    redirect_authenticated_user = True
    template_name = 'auth/signin.html'


class SignOutView(LogoutView):

    def get_success_url(self):
        return reverse_lazy('core:index')


class PasswordChangeView(DefaultPasswordChangeView):
    template_name = 'auth/passwords/change_password.html'
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response # TODO: messages
