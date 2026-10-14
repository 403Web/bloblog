from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView

from .views import (
    SignUpView,
    EmailVerificationView,
    ResendVerificationView,
    SignInView,
    SignOutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
    ResendPasswordResetView
)


app_name = 'accounts'


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verification/resend/', ResendVerificationView.as_view(), name='resend_verification'),
    path('verification/<uidb64>/<token>/', EmailVerificationView.as_view(), name='email_verification'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', SignOutView.as_view(), name='signout'),

    path('change-password/', PasswordChangeView.as_view(), name='change_password'),

    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
    path(
        'reset-password/email-sent/',
        PasswordResetDoneView.as_view(
            template_name='auth/passwords/reset/email_sent.html'
        ),
        name='reset_password_done'
    ),
    path(
        'reset-password/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='reset_password_confirm'
    ),
    path('reset-password/resend/', ResendPasswordResetView.as_view(), name='resend_reset_password')
]
