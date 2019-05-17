from django.urls import path
from . import views


urlpatterns = [
    path('Curator', views.content_view, name='contentform'),
    path('Detail/<int:pk>/<slug:slug>', views.content_details, name='content_details'),
    path('Edit_content/<int:pk>/<slug:slug>', views.edit_content, name='edit_content'),
    path('Content_Main/', views.main_page, name='main_page'),
    path('Curator_Profile/<int:content_id>/', views.content_creator_profile, name='curator_profile'),
    path('Publish/<int:pk>/', views.to_publish, name='publish'),


]
