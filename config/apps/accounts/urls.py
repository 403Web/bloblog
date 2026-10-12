from django.urls import path

from .views import (
    SignUpView,
    EmailVerificationView,
    ResendVerificationView,
    SignInView,
    SignOutView
)


app_name = 'accounts'


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verification/resend/', ResendVerificationView.as_view(), name='resend_verification'),
    path('verification/<uidb64>/<token>/', EmailVerificationView.as_view(), name='email_verification'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', SignOutView.as_view(), name='signout')
]
