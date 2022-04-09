import os

from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'persia_atlas.settings')

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from products.websocket.routing import websocket_urlpatterns as robot_urls
from products.websocket.middleware import TokenAuthMiddleware


application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter(
            robot_urls
        )
    )
})
