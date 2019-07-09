from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:pk>/follower', views.user_follow, name='user_follow')]
