from django.forms import ModelForm
from .models import CourseMaterial, PastQuestion
from django import forms


class FormForMaterial(ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['file', 'course_code', 'course_title', 'material_title', 'shared_by']


class FormForQuestion(ModelForm):
    class Meta:
        model = PastQuestion
        fields = ['image', 'file', 'course_code', 'course_title', 'school']
        widgets = {"image": forms.ClearableFileInput(attrs={'id': 'image', 'multiple': True})}

   

class FormForReviewing(ModelForm):
    class Meta:
        model = PastQuestion
        fields = ['review']






