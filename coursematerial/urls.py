from django.urls import path
from . import views


urlpatterns = [
    path('UploadQuestion/', views.FormForPastQuestion.as_view(), name='upload_question'),
    path('UploadMaterial/', views.form_for_material_view, name='upload_material'),
    path('DownloadQuestion/<int:pk>/', views.past_question_view, name='download_question'),
    path('ReviewQuestion/', views.question_review_form, name='question_review'),
    path('EditReviewQuestion/<int:pk>/', views.edit_review_question, name='edit_question_review'),
    path('DownloadMaterial/<int:pk>/', views.download_material, name='download_material'),

]