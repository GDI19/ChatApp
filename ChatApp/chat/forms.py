from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ChatUser


class ChatUserRegistrationForm(UserCreationForm):
    class Meta:
        model = ChatUser
        fields = ["username","first_name", "last_name", "phone", "email", "password1", "password2"]


class ChatUserUpdateProfile(forms.ModelForm):
    class Meta:
        model = ChatUser
        fields = ["first_name", "last_name", "phone", "email"]

