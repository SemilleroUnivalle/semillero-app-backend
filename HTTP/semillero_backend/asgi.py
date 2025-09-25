import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'semillero_backend.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import estudiante.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            estudiante.routing.websocket_urlpatterns
        )
    ),
})