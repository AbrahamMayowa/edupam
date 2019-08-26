from django.db import models
from django.utils import timezone
from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Q


class PostManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            qs_look = (
                Q(title__icontains=query)|
                Q(author__icontains=query)
            )
            unique_qs = qs.filter(qs_look).distinct()
        return unique_qs



class Post(models.Model):
    category_lists = (
        ('academic', 'Academic'),
        ('opportunity', 'Opportunity'),
        ('business_hub', 'Business Hub'),
        ('admission', 'Admission'),
        ('politics', 'Politics'),
        ('award_competition', 'Awards and Competition'),
        ('relationship', 'Relationship'),
        ('social_life', 'Campus Social Life'),
        ('creative_writing', 'Creative Writing'),
        ('general', 'General'),
        ('nysc', 'NYSC')
    )
    title = models.CharField(max_length=150, blank=False, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = RichTextField()
    slug = models.SlugField(max_length=150, unique=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    category = models.CharField(max_length=50, blank=False, choices=category_lists)
    view_number = models.IntegerField(default=0)
    user_followed = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed_post')
    post_thumped_up = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='thumped_up_actors')
    post_thumped_down = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='thumped_down_actors')
    post_hidden = models.BooleanField(default=False)
    user_array_flag_post = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_user_flag')

    objects = PostManager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_details', kwargs={'pk': self.pk, 'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def class_name(self):
        return self.__class__.__name__



class Picture(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_pictures')
    image = models.ImageField(upload_to='post_image', blank=True, null=True)



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(max_length=2000, blank=False, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    comment_hidden = models.BooleanField(default=False)
    comment_thumped_up = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_thumped_up')
    comment_thumped_down = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_thumped_down')
    user_array_flag_comment = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_user_flag')

class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=2000, blank=False, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    comment_reply_hidden = models.BooleanField(default=False)
    reply_thumped_up = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='replies_thumped_up')
    reply_thumped_down = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='replies_thumped_down')
    user_array_flag_comment_reply = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='reply_flag')

class CommentPicture(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_pictures')
    picture = models.ImageField(upload_to='forum_comment_image', blank=True, null=True)