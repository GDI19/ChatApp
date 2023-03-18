import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers

from .forms import ChatUserRegistrationForm
from .models import ChatRoom


def get_chat_rooms_list():
    return ChatRoom.objects.all().values()

@login_required()
def index(request):
    context = {
        'chat_rooms_list': get_chat_rooms_list(),
    }
    return render(request, 'chat/index.html', context)

def registration(request):
    if request.method == 'POST':
        form = ChatUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! Your account has been created! To enter Chat App you need to login.')
            return redirect('login')
    else:
        messages.error(request, 'Unsuccessful registration. Invalid information.')
        form = ChatUserRegistrationForm()

    context = {'form': form}
    return render(request, 'chat/register.html', context)


@login_required()
def room(request, room_name):
    room_name_in_db = ChatRoom.objects.filter(name=room_name).values()
    if not room_name_in_db:
        created_room = ChatRoom(name=room_name)
        created_room.save()
        room_id = created_room.pk
    else:
        room_id = room_name_in_db[0]['id']

    context = {
        'room_name': room_name,
        'room_id': room_id,
        'username': request.user.username,
        'chat_rooms_list': get_chat_rooms_list(),
    }

    return render(request, 'chat/room.html', context)

