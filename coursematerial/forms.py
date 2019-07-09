from django.forms import ModelForm
from .models import FileUpload, FileReview, CourseFile
from haystack.forms import SearchForm
from django import forms

"""
class MaterialForm(ModelForm):

    class Meta:
        model = CourseMaterial
        fields = ['course_code', 'course_title', 'material_title', 'school', 'department', ]
"""


class FileForm(ModelForm):

    class Meta:
        model = FileUpload
        fields = ['course_code', 'course_title', 'school_name', 'department', 'file_type' ]

   

class FileReviewForm(ModelForm):

    class Meta:
        model = FileReview
        fields = ['review']

#past question file upload
class FileUploadForm(ModelForm):

    class Meta:
        model = CourseFile
        fields = ['course_file']









