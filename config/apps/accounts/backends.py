from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


User = get_user_model()


class AuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = username or kwargs.get('email')

        if not identifier or not password:
            return None

        user = None

        try:
            user = User.objects.get(username__iexact=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email__iexact=identifier)
            except User.DoesNotExist:
                User().set_password(password)
                return None

        if (
            user.check_password(password) and
            self.user_can_authenticate(user)
        ):
            return user

        return None
