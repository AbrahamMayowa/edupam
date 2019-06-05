from django.forms import ModelForm
from .models import Journalism, Comment


class ContentForm(ModelForm):

    class Meta:
        model = Journalism
        fields = ['title', 'content',]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_body']





