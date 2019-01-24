from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models



class Post(models.Model):
    category_lists = (
        ('academic', 'Academic'),
        ('opportunity', 'Opportunity'),
        ('business_hub', 'Business Hub'),
        ('admission', 'Admission'),
        ('politics', 'Politics'),
        ('award', 'Awards'),
        ('relationship', 'Relationship'),
        ('events', 'Events'),
        ('knowledge', 'Knowledge'),
        ('creative_writing', 'Creative Writing'),
        ('general', 'General'),
    )
    title = models.CharField(max_length=40, blank=False, null=False, default='Your post title')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = models.CharField(max_length=1000, blank=False, null=False)
    published_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, blank=False, choices=category_lists)
    view_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Picture(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='post_image', blank=True, null=True)

    def __str__(self):
        return self.post.title + 'image'




class Like(models.Model):
    like_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    number_of_likes = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=1000, blank=False, null=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='post_image')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text







# Create your models here.
