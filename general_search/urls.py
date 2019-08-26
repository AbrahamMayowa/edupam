from django.urls import path
from . import views

urlpatterns = [
    path('search', views.general_search, name='general_search')
]