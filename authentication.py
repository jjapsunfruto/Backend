from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import close_old_connections
import jwt

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return JWTAuthMiddlewareInstance(scope, self.inner)

class JWTAuthMiddlewareInstance:
    def __init__(self, scope, inner):
        self.scope = scope
        self.inner = inner

    async def __call__(self, receive, send):
        headers = dict(self.scope['headers'])
        close_old_connections()

        if b'authorization' in headers:
            token_name, token_key = headers[b'authorization'].decode().split()
            if token_name.lower() == 'bearer':
                try:
                    validated_token = JWTAuthentication().get_validated_token(token_key)
                    user = JWTAuthentication().get_user(validated_token)
                    self.scope['user'] = user
                except jwt.ExpiredSignatureError:
                    self.scope['user'] = AnonymousUser()
                except jwt.InvalidTokenError:
                    self.scope['user'] = AnonymousUser()
        else:
            self.scope['user'] = AnonymousUser()

        return await self.inner(self.scope, receive, send)
