from django.db import models
from django.contrib.auth.models import AbstractUser


class ChatUser(AbstractUser):
    phone = models.IntegerField(default=789)
    # class Meta:
    #   verbose_name_plural = 'ChatUsers'
