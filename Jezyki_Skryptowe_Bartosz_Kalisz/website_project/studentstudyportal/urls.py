from django.contrib import admin
from django.urls import path, include
from dashboard import views as dash_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('dashboard.urls')),
    path('zarejestruj/',dash_views.zarejestruj,name='zarejestruj'),
    path('zaloguj/',
    auth_views.LoginView.as_view(template_name='dashboard/zaloguj.html'),
    name='zaloguj'),
    path('wyloguj/',
    auth_views.LogoutView.as_view(template_name='dashboard/wyloguj.html'),
    name='wyloguj'),
    path('użytkownik/',dash_views.użytkownik,name='użytkownik'),
]
