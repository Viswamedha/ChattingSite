from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
  re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatRoomConsumer.as_asgi()), # Using asgi
  re_path(r'^ws/testing/$', consumers.NewConsumer.as_asgi()),
]
