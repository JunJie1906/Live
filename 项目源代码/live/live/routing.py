from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter



import liveapp.routing


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            liveapp.routing.websocket_urlpatterns
        )
    )
})