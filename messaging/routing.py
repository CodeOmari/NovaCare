from django.urls import re_path
from . import consumers

# Match WebSocket URLs to specific consumers
# websocket_urlpatterns is imported by the asgi.py file to set up the WebSocket Router
websocket_urlpatterns = [
    re_path(r'ws/message/(?P<conversation_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
