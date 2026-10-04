from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import SignUpForm


User = get_user_model()


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        super().form_valid(form)

        login(self.request, self.object)
        # email verification

        return redirect(reverse_lazy('core:index'))
        # return render(self.request, 'auth/email_verification/email_sent.html')


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('core:index'))

        return super().get(request, *args, **kwargs)


class SignInView(LoginView):
    redirect_authenticated_user = True
    template_name = 'auth/signin.html'


class SignOutView(LogoutView):

    def get_success_url(self):
        return reverse_lazy('core:index')
