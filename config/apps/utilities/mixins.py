from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages


class VerificationRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return False if not self.request.user.is_verified else True

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(
            self.request,
            'You need to verify your account first.',
            extra_tags='danger'
        )
        return redirect(self.request.META.get('HTTP_REFERER'))
