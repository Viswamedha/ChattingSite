


from django.urls import path

from .views import *

urlpatterns = [
    path('', all_chats),
    path('<slug:room_name>/', room, name = 'room')
]