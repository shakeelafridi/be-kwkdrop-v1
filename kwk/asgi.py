# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import bagger.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kwk.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            bagger.routing.websocket_urlpatterns
        )
    ),
})