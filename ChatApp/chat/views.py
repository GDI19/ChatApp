import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers

from .forms import ChatUserRegistrationForm
from .models import ChatRoom, RoomMessage


@login_required()
def index(request):
    return render(request, 'chat/index.html')

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
    print(room_name_in_db)
    if not room_name_in_db:
        created_room = ChatRoom(name=room_name)
        created_room.save()
        room_id = created_room.pk
    else:
        room_id = room_name_in_db[0]['id']

    context = {'room_name': room_name, 'room_id': room_id, 'username': request.user.username}

    return render(request, 'chat/base.html', context)

def messages_to_json(messages):
    result = []
    for message in messages:
        result.append(message_to_json(message))
    return result

def message_to_json(message):
    return {
        'sender': message.sender.username,
        'body': message.body,
        'published': str(message.published)
    }