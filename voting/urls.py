from django.urls import path
from . import views


urlpatterns = [
    path('award/', views.award_view, name='award_view'),
    path('award/<int:pk>/result/', views.result_view, name='result_view'),
    path('award/voting/', views.saving_vote, name='saving_view'),
    path('award_list/', views.award_list, name='award_list'),
    path('award/category/<int:pk>/', views.category_details, name='category_details'),
    path('award_details/<int:pk>/', views.award_details, name='award_details'),
    path('get_award/<int:pk>/', views.get_award, name='get_award'),


]