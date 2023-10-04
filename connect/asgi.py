"""
ASGI config for myclub_website project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""


import os

from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
from chat_app.routing import websocket_urlpatterns
from reservation.routing import Re_websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'connect.settings')
django_asgi_app = get_asgi_application()

# application = get_asgi_application()

application = ProtocolTypeRouter({
        'http':django_asgi_app,

        'websocket':AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter( 
                    websocket_urlpatterns + Re_websocket_urlpatterns
            )
        )
        )
})

 
