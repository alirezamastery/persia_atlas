from django.urls import path

from .consumers import RobotConsumer

websocket_urlpatterns = [
    path('ws/', RobotConsumer.as_asgi()),
]
