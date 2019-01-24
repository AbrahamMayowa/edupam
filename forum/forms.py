from django.forms import ModelForm
from django import forms


from .models import Comment, Post, Picture


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'category']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'picture']


class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['image']

