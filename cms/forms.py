from django.forms import ModelForm
from .models import Journalism, Comment, CommentReply


class ContentForm(ModelForm):

    class Meta:
        model = Journalism
        fields = ['title', 'content', 'post_status']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_body']

class CommentReplyForm(ModelForm):
    class Meta:
        model = CommentReply
        fields = ['reply']





