import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from notification.routing import websocket_urlpatterns
from authentication.middleware import JWTAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KKaebiBack.settings')

# Django ASGI 앱 초기화
django_asgi_app = get_asgi_application()

# ASGI 애플리케이션 정의
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddlewareStack(
        URLRouter(websocket_urlpatterns),
    ),
})
