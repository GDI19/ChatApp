from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ChatUser


class ChatUserRegistrationForm(UserCreationForm):
    class Meta:
        model = ChatUser
        fields = ["username", "email", "password1", "password2"]