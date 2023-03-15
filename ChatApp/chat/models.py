from django.db import models
from django.contrib.auth.models import AbstractUser


class ChatUser(AbstractUser):
    phone = models.IntegerField(default=789)
    # class Meta:
    #   verbose_name_plural = 'ChatUsers'
    def __str__(self):
        return self.username

class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    published = models.DateTimeField(auto_now_add=True)
    # published.editable = True

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.sender.__str__()


class RoomMessage(Message):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

    def __str__(self):
        return 'To '+ self.room.name +' from '+ self.sender.__str__()

    def get_20_messages(room_id):
        messages = RoomMessage.objects.filter(room=ChatRoom(id=room_id))[:20]
        reversed_messages = reversed(messages)
        return reversed_messages

