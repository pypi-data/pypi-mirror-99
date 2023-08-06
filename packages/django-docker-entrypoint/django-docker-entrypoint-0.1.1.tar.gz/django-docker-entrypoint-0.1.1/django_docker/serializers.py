from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email')


class SessionSerializer(serializers.Serializer):
    session_key = serializers.CharField(allow_null=True)
    user = serializers.DictField(allow_null=True)

    @staticmethod
    def _get_user(user):
        if not user:
            return None
        serializer = UserSerializer(user)
        return serializer.data

    def __init__(self, **kwargs):
        kwargs.update({'data': {'session_key': kwargs['data'].get('session_key'),
                                'user': self._get_user(kwargs['data'].get('user'))}})
        super().__init__(**kwargs)


class RequestSerializer(serializers.Serializer):
    ip = serializers.IPAddressField(required=False)
    method = serializers.CharField(max_length=20)
    user_agent = serializers.CharField(max_length=500)
    path = serializers.CharField()
    request_meta = serializers.DictField(required=False)
    authenticated = serializers.BooleanField(default=False)
    session = serializers.DictField(required=False)

    @staticmethod
    def _get_meta(meta: dict) -> dict:
        serialized_meta = {}
        for key, value in meta.items():
            if key.startswith(('HTTP', 'REQUEST', 'REMOTE')):
                serialized_meta[key] = value
        return serialized_meta

    @staticmethod
    def _get_session(session, user):
        serializer = SessionSerializer(
            data={'session_key': session.session_key, 'user': user if not isinstance(user, AnonymousUser) else None})
        return serializer.validated_data if serializer.is_valid(raise_exception=True) else None

    def __init__(self, **kwargs):
        request = kwargs['context']['request']
        kwargs.update(
            {
                'data': {
                    'ip': request.META.get(
                        'HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')
                    ),
                    'method': request.META.get('REQUEST_METHOD'),
                    'user_agent': request.META.get('HTTP_USER_AGENT'),
                    'path': request.path_info,
                    'authenticated': request.user.is_authenticated,
                    'session': self._get_session(session=request.session, user=request.user),
                    'request_meta': self._get_meta(dict(request.META)),
                }
            }
        )
        super().__init__(**kwargs)
