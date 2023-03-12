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
    if not room_name_in_db:
        created_room = ChatRoom(name=room_name)
        created_room.save()
        room_id = created_room.pk
    else:
        room_id = room_name_in_db[0]['id']
    #all_room_messages = RoomMessage.objects.filter(room=ChatRoom(id=room_id)).values('sender', 'body')
    #if all_room_messages:
    #    all_room_messages_json = serializers.serialize('json', all_room_messages)
    #else:
    #    all_room_messages_json = {}
    context = {'room_name': room_name, 'room_id': room_id}
    #print(all_room_messages)
    return render(request, 'chat/room.html', context)