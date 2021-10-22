from os import name
from django.urls import path
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
from . import views


urlpatterns = [
  path(_('login/'), views.user_login, name='login'),
  path(_('logout/'), auth_views.LogoutView.as_view(), name='logout'),
  path(_('register/'), views.register, name='register'),
  path(_('profile/'), views.profile, name='profile'),
  
  path(_('password_change/'), auth_views.PasswordChangeView.as_view(),
    name='password_change'),
  
  path(_('password_change/done/'), auth_views.PasswordChangeDoneView.as_view(),
    name='password_change_done'),
  
  path(_('password_reset/'), auth_views.PasswordResetView.as_view(), 
    name='password_reset'),

  path(_('password_reset/done/'), auth_views.PasswordResetDoneView.as_view(),
    name='password_reset_done'),

  path('password_reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(), 
    name='password_reset_confirm'),
  
  path(_('password_reset/complete/'), 
    auth_views.PasswordResetCompleteView.as_view(),
    name='password_reset_complete'),
]