import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import tempochat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tempochat.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            tempochat.routing.websocket_urlpatterns
        )
    ),
})