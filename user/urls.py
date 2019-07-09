from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('profile/<int:pk>/update', views.update_user_info, name='profile_edit'),
    path('profile/<int:pk>/picture', views.upload_profile_picture, name='profile_picture'),
    path('profile/<int:pk>/header', views.upload_header_picture, name='profile_header'),
    path('profile/<int:pk>', views.user_profile, name='user_info'),
    path('Welcome/<int:pk>', views.welcome_page, name='welcome'),
    

]