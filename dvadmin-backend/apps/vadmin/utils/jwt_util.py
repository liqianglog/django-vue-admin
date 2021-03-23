import uuid
from calendar import timegm
from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth import login


def jwt_response_payload_handler(token, user, request):
    """
    重写JWT的返回值
    :param token:
    :param user:
    :param request:
    :return:
    """
    login(request, user)
    return {
        'token': f"{token}",
    }


def jwt_get_session_id(token=None):
    """
    获取会话id
    :param token:
    :return:
    """
    payload = jwt.decode(token, None, False)
    if isinstance(payload, dict):
        return payload.get("session_id", "")
    return getattr(payload, "session_id", "")


def jwt_get_user_secret_key(user):
    """
    重写JWT的secret的生成
    :param user:
    :return:
    """
    return str(user.secret)

def jwt_payload_handler(user):
    payload = {
        'user_id': user.pk,
        'username': user.username,
        'session_id': str(uuid.uuid4()),
        'exp': datetime.utcnow() + settings.JWT_AUTH.get('JWT_EXPIRATION_DELTA')
    }
    if settings.JWT_AUTH.get('JWT_ALLOW_REFRESH'):
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )
    if settings.JWT_AUTH.get('JWT_AUDIENCE',None) is not None:
        payload['aud'] = settings.JWT_AUTH.get('JWT_AUDIENCE',None)
    if settings.JWT_AUTH.get('JWT_ISSUER',None) is not None:
        payload['iss'] = settings.JWT_AUTH.get('JWT_ISSUER',None)
    return payload
