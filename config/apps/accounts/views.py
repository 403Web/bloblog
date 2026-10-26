from django.views.generic.base import View, RedirectView
from django.views.generic import CreateView
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView as DefaultPasswordChangeView,
    PasswordResetView as DefaultPasswordResetView,
    PasswordResetConfirmView as DefaultPasswordResetConfirmView
)
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from apps.accounts.models import Profile
from apps.blog.models import Post
from django.conf import settings
from django.contrib import messages

from .models import Follow
from .forms import SignUpForm, PasswordResetForm, ProfileUpdateForm


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{user.email}{user.is_verified}{timestamp}'


User = get_user_model()
email_verification_token = EmailVerificationTokenGenerator()


def send_email(request, user, template_name):
    token = email_verification_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    context = {
        'user': user,
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': request.get_host(),
        'uid': uid,
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
            login(request, user)
            messages.success(
                request,
                'Your email has been verified successfully.',
                extra_tags='success'
            )
            return redirect(reverse_lazy('core:index'))
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

        if not logged_in:
            return redirect(reverse_lazy('accounts:signin'))

        if logged_in:
            messages.info(
                request,
                'Your account is already verified.',
                extra_tags='warning'
            )
            return redirect(reverse_lazy('core:index'))


class SignInView(LoginView):
    redirect_authenticated_user = True
    template_name = 'auth/signin.html'

    def form_valid(self, form):
        messages.success(
            self.request,
            'You have signed in successfully. Welcome back!',
            extra_tags='success'
        )
        return super().form_valid(form)


class SignOutView(LogoutView):

    def get_success_url(self):
        messages.success(
            self.request,
            'You have been signed out successfully.',
            extra_tags='primary'
        )
        return reverse_lazy('core:index')


class PasswordChangeView(DefaultPasswordChangeView):
    template_name = 'auth/passwords/change_password.html'
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Your password has been changed successfully.',
            extra_tags='success'
        )
        return response


class PasswordResetView(DefaultPasswordResetView):
    form_class = PasswordResetForm
    template_name = 'auth/passwords/reset/email_get.html'
    email_template_name = 'auth/passwords/reset/reset_password.html'
    success_url = reverse_lazy('accounts:reset_password_done')


class PasswordResetConfirmView(DefaultPasswordResetConfirmView):
    template_name = 'auth/passwords/reset/reset_confirm.html'
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Your password has been reset successfully.',
            extra_tags='success'
        )
        return response


class ResendPasswordResetView(RedirectView):
    url = reverse_lazy('accounts:reset_password')


class FollowView(View):

    def post(self, request, pk, *args, **kwargs):
        user = Profile.objects.get(pk=pk)

        if user != request.user.profile:
            follow, created = Follow.objects.get_or_create(
                following=user,
                follower=request.user.profile
            )

            if not created:
                follow.delete()

        return redirect(request.META.get('HTTP_REFERER', reverse_lazy('accounts:settings')))


class ProfileView(View):

    def get(self, request, pk, *args, **kwargs):
        data = get_object_or_404(Profile, pk=pk)

        if request.user.is_authenticated:
            if data == request.user.profile:
                return redirect('accounts:settings')

        if data.user.email == settings.DELETED_USER_EMAIL:
            return redirect('accounts:settings')

        context = {
            'data': data,
            'followed': (
                True if Follow.objects.filter(
                    following=data,
                    follower=request.user.profile
                ).exists() else False
            ) if request.user.is_authenticated else False
        }
        return render(request, 'auth/profile.html', context)


class ProfilePreview(View):

    def get(self, request, *args, **kwargs):
            data = request.user.profile
    
            context = {
                'data': data,
                'me': True,
                'followed': (
                    True if Follow.objects.filter(
                        following=data,
                        follower=request.user.profile
                    ).exists() else False
                ) if request.user.is_authenticated else False
            }
            return render(request, 'auth/profile.html', context)


class SettingsView(View):

    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(author=request.user.profile)
        return render(request, 'auth/settings.html', {'posts': posts})

    def post(self, request, *args, **kwargs):
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Profile updated successfully.',
                extra_tags='success'
            )
            return redirect('accounts:settings')

        messages.error(
            request,
            'Failed to updated profile. Please try again later.',
            extra_tags='danger'
        )
        return redirect('accounts:settings')
