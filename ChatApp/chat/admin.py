from django.contrib import admin
from .models import ChatUser, ChatRoom, RoomMessage

admin.site.register([ChatUser, ChatRoom, RoomMessage])