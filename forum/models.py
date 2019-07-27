from django.db import models
from django.utils import timezone
from django.db import models
from django.conf import settings



class Post(models.Model):
    category_lists = (
        ('academic', 'Academic'),
        ('opportunity', 'Opportunity'),
        ('business_hub', 'Business Hub'),
        ('admission', 'Admission'),
        ('politics', 'Politics'),
        ('award', 'Awards'),
        ('relationship', 'Relationship'),
        ('social_life', 'Social Life'),
        ('creative_writing', 'Creative Writing'),
        ('general', 'General'),
        ('youth_service', 'Youth Service')
    )
    title = models.CharField(max_length=50, blank=False, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=3000, blank=False, null=False)
    published_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, blank=False, choices=category_lists)
    view_number = models.IntegerField(default=0)
    user_followed = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed_post')
    thumped_up = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='thumped_up')
    thumped_down = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='thumped_down')


    def __str__(self):
        return self.title


class Picture(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_image', blank=True, null=True)



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000, blank=False, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    thumped_up = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_thumped_up')
    thumped_down = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_thumped_down')


    def __str__(self):
        return self.text

class CommentPicture(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_pictures')
    picture = models.ImageField(upload_to='comment_image')