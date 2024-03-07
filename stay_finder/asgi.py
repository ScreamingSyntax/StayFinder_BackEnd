import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from stay_finder.routing import websocket_urlpatterns  # Ensure 'myproject' matches your Django project name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stay_finder.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(), 
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
