from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class CertModelBackend(ModelBackend):
    """
    This is a Backed that allows authentication
    with cert_no address or certNo.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = get_user_model().objects.get(cert_no=username)
            if user.check_password(password):
                return user
            else:
                return None
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(cert_no=username)
        except get_user_model().DoesNotExist:
            return None