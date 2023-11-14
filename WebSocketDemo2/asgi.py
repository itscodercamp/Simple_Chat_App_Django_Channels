import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import ChatApp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebSocketDemo2.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(), 
    'websocket': URLRouter(ChatApp.routing.websocket_urlpatterns),
})
