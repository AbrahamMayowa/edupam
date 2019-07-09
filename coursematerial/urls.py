from django.urls import path
from . import views


urlpatterns = [
    path('file/<int:pk>', views.file_detail, name='file_detail'),
    path('course|file/review/<int:pk>', views.file_review, name='file_review'),
    path('course|file/review/edit/<int:question_id>/<int:review_id>', views.edit_file_review, name='edit_file_review'),
    path('download/<int:pk>/<path:path>', views.file_download, name='download_file'),
    path('course/info', views.file_info, name='course_file_upload'),
    path('course/<int:pk>/file', views.file_upload_view, name='file_upload_view'),
    path('upload/<int:pk>/upload', views.file_upload_ajax, name='file_ajax_upload'),


]