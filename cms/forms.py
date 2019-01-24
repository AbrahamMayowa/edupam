from django.forms import ModelForm
from .models import Journalism


class ContentForm(ModelForm):

    class Meta:
        model = Journalism
        fields = ['title', 'content']




