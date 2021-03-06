from django.forms import ModelForm
from django import forms


from . models import Comment, Post, Picture, CommentPicture, CommentReply


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'category']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class CommentPictureForm(ModelForm):
    class Meta:
        model = CommentPicture
        fields = ['picture']


class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['image']


class ReplyForm(ModelForm):
    class Meta:
        model = CommentReply
        fields = ['body']

