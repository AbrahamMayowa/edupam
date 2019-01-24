from django.urls import path
from . import views


urlpatterns = [
    path('', views.content_view, name='contentform'),
    path('<int:pk>/', views.content_details, name='content_details'),
    path('edit_content/<int:pk>/', views.edit_content, name='edit_content'),
    path('content_main/<int:pk>/', views.content_main, name='content_main'),

]
