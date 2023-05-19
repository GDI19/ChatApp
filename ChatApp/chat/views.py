import json
from django.core.mail import EmailMessage, send_mail, BadHeaderError

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.models.query_utils import Q
from django.core import serializers

from .forms import ChatUserRegistrationForm, ChatUserUpdateProfile
from .models import ChatRoom, ChatUser
from .tokens import account_activation_token


@login_required()
def index(request):
    context = {
        'chat_rooms_list': get_chat_rooms_list(),
        'user_profile': get_update_profile(request),
    }
    return render(request, 'chat/index.html', context)


def registration(request):
    form = ChatUserRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # messages.success(request, 'Congratulations! Your account has been created! To enter Chat App you need to login.')
            activate_email(request, user, form.cleaned_data.get('email'))
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

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
        'chat_rooms_list': get_chat_rooms_list(),
        'user_profile': get_update_profile(request),
    }

    return render(request, 'chat/room.html', context)


def get_chat_rooms_list():
    return ChatRoom.objects.all().values()


def get_update_profile(request):
    user = request.user
    user_profile = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
        'email': user.email,
        'image': user.image,
    }

    profile_form = ChatUserUpdateProfile(request.POST or None, request.FILES, instance=user)

    if request.method == 'POST':
        if profile_form.is_valid():
            profile_form.save()
            user_profile = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'email': user.email,
                'image': user.image,
                'profile_form': profile_form,
            }

            messages.success(request, 'Your profile has been updated!')
            return user_profile

        for error in list(profile_form.errors.values()):
            messages.error(request, error)

    user_profile['profile_form'] = profile_form
    return user_profile


def activate_email(request, user, to_email):
    mail_subject = 'Activate your user account.'
    msg_body = render_to_string('template_activate_account.html', {
        'username': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })

    mail_msg = EmailMessage(mail_subject, msg_body, to=[to_email])
    if mail_msg.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = ChatUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('register')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = ChatUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Request"
                    email_template_name = "chat/password/password_reset_email.txt"
                    context_to_email = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Group Chat',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					    'user': user,
                        'token': default_token_generator.make_token(user),
    					'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, context_to_email)
                    try:
                        send_mail(subject, email, 'admin@example.com',[user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')

                    return redirect("/password_reset/done/")
        messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="chat/password/password_reset.html",
                                  context={"password_reset_form": password_reset_form})

