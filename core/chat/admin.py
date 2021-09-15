from django.contrib import admin
from .models import *

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):


    pass 


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):


    pass
