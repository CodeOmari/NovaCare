from django.urls import re_path
from . import consumers

# Match WebSocket URLs to specific consumers
websocket_urlpatterns = [
    re_path(r'ws/message/(?P<conversation_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
