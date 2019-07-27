from django.contrib import admin
from .models import Comment, Post, Picture, CommentPicture

admin.site.register(Comment)
admin.site.register(CommentPicture)
admin.site.register(Post)
admin.site.register(Picture)


# Register your models here.
