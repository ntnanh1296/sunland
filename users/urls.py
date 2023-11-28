# users/urls.py
from django.urls import path

from .views import register_user, login_user

urlpatterns = [
    path('register/', register_user, name='regiser_user'),
    path('login/', login_user, name='login_user'),
]