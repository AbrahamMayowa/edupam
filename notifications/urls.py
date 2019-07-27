from django.urls import path
from . import views


urlpatterns = [
    path('Notifications/<int:user_id>', views.update_view_status, name='user_notification'),
    
]