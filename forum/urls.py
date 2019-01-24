from django.urls import path
from . import views

urlpatterns = [
    path('post_form/', views.post_form_view, name='post_form'),
    path('post/<int:pk>/', views.post_details, name='post_details'),
    path('post/academic/', views.academic_post_view, name='academic_post'),
    path('post/opportunity/', views.opportunity_post_view, name='opportunity_post'),
    path('post/business/', views.business_hub_view, name='business_post'),
    path('post/admission/', views.admission_view, name='admission_post'),
    path('post/events/', views.events_view, name='events_post'),
    path('post/politics/', views.politics_view, name='politics_post'),
    path('post/award/', views.award_view, name='award_post'),
    path('post/relationship/', views.relationship_view, name='relationship_post'),
    path('post/knowledge/', views.knowledge_view, name='knowledge_post'),
    path('post/creative_writing/', views.creative_writing_view, name='creative_writing_post'),
    path('post/general/', views.general_view, name='general_post'),


]