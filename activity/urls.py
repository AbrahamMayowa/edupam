from django.urls import path
from . import views

urlpatterns = [
    path('Activity/<int:user_id>', views.user_activities, name='activity'),
    
]