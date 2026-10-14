from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm as DefaultPasswordResetForm
from mail_templated import EmailMessage
from django.contrib.auth import get_user_model
from apps.accounts.models import Profile


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']


class PasswordResetForm(DefaultPasswordResetForm):

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None
    ):
        email = EmailMessage(email_template_name, context, from_email, to=[to_email])
        email.send()


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name', 'avatar']
