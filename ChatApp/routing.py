from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path('ws/sync/<str:group_name>/' , consumer.MySyncConsumer.as_asgi()),
]