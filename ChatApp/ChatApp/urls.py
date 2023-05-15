from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from chat.views import registration, get_update_profile, activate

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='chat/login.html')),
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('register/', registration, name='register' ),
    path('login/', auth_views.LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='chat/logout.html'), name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('accounts/', include('allauth.urls')),
    # path('profile/', get_update_profile , name='user_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
