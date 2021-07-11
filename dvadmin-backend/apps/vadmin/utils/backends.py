import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication as DjangoSessionAuthentication

logger = logging.getLogger(__name__)
UserModel = get_user_model()


class CustomBackend(ModelBackend):
    """
    Django原生认证方式
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        msg = '%s 正在使用本地登录...' % username
        logger.info(msg)
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                user.last_login = timezone.now()
                user.save()
                return user


class SessionAuthentication(DjangoSessionAuthentication):
    """
    Session认证
    """

    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """
        # Get the session-based user from the underlying HttpRequest object
        user = getattr(request._request, 'user', None)
        # Unauthenticated, CSRF validation not required
        if not user or not user.is_active:
            return None
        # self.enforce_csrf(request)
        # CSRF passed with authenticated user
        return user, None
