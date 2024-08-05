# chat/routing.py
from django.urls import re_path
from . import consumers  # Adjust the import to where your consumer is located

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
