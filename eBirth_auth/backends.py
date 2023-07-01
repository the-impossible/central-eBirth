from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend, BaseBackend

class CertModelBackend(BaseBackend):
    """
    This is a Backed that allows authentication
    with email address or certNo.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = get_user_model().objects.get(cert_no=username.upper())
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(user_id=username)
        except get_user_model().DoesNotExist:
            return None