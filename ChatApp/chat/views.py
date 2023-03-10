from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ChatUserRegistrationForm


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
    return render(request, 'chat/room.html', {'room_name': room_name} )