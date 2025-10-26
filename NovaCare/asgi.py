"""
ASGI config for NovaCare project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# from messages.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NovaCare.settings')


# Define how to handle different connection types (HTTP, WebSocket, etc.)
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Normal Django HTTP requests
    "websocket": AuthMiddlewareStack(  # For WebSocket connections (chat)
        URLRouter(websocket_urlpatterns)  # Route WebSocket URLs to consumers
    ),
})


# ProtocolTypeRouter directs traffic --HTTP request to go to Django, WebSockets connectons go to our chat
# AuthMiddlewareStack keeps user authentication active during a WebSocket connection
# URLRouter loads WebSocket from our chat app
