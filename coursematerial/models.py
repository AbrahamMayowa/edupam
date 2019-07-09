from django.db import models
from django.conf import settings
from django.utils import timezone





class FileUpload(models.Model):

    UPLOAD_TYPE = (
    ('past_question', 'Past Question'),
    ('course_material', 'Course Material')
    )
    course_code = models.CharField(max_length=50, null=False, blank=False)
    course_title = models.CharField(max_length=100, null=False, blank=False)
    school_name = models.CharField(max_length=100, null=False, blank=False)
    department = models.CharField(max_length=100, null=False, blank=False)
    time_of_download = models.IntegerField(default=0)
    upload_time = models.DateField(auto_now_add=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=50, choices=UPLOAD_TYPE, null=False, blank=False)



class CourseFile(models.Model):
    file_info = models.ForeignKey(FileUpload, on_delete=models.CASCADE, related_name='file_info')
    course_file = models.FileField(blank=True, null=True, upload_to='course_file')


class FileReview(models.Model):
    course_file = models.ForeignKey(FileUpload, on_delete=models.CASCADE, related_name='course_file')
    review = models.TextField(max_length=1000, null=False, blank=False)
    review_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_time = models.DateField(auto_now_add=True)

"""
class CourseMaterial(models.Model):
    course_title = models.CharField(max_length=200, blank=False, null=False)
    course_code = models.CharField(max_length=50, blank=False, null=False)
    material_title = models.CharField(max_length=200, null=True, blank=True)
    school = models.CharField(max_length=200, null=False, blank=False)
    department = models.CharField(max_length=200, null=False, blank=False)
    time_of_download = models.IntegerField(default=0)
    upload_time = models.DateField(auto_now_add=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class MaterialFile(models.Model):
    course_material_data = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE, related_name='course_material_file')
    course_file = models.FileField(upload_to='course_material', null=False, blank=False)

class MaterialReview(models.Model):
    course_material = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE, related_name='course_material_review')
    review = models.TextField(max_length=1000, null=False, blank=False)
    review_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)

"""








# Create your models here.
