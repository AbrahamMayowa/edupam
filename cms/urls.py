from django.urls import path
from . import views


urlpatterns = [
    path('Curator', views.content_view, name='contentform'),
    path('Detail/<int:pk>/<slug:slug>', views.content_details, name='content_details'),
    path('Edit_content/<int:pk>/<slug:slug>', views.edit_content, name='edit_content'),
    path('Content_Main/', views.main_page, name='main_page'),
    path('Curator/Profile/<int:pk>', views.content_creator_profile, name='curator_profile'),
    path('comment/<int:pk>/', views.comment_view, name='content_comment'),
    path('content/claps/<int:pk>', views.clap, name='clap'),
    path('delete/<int:pk>', views.delete_content, name='delete_content'),
    path('delete/confirm/<int:pk>', views.redirect_delete, name='redirect_delete'),
    path('delete/comment/<int:comment_pk>/<int:journalist_id>', views.delete_comment, name='delete_comment'),
    path('comment/thumpUp/<int:pk>', views.comment_thump_up, name='comment_thump_up'),
    path('comment/thumpup/<int:pk>', views.comment_thump_down, name='comment_thump_down'),


]