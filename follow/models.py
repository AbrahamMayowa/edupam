from django.db import models
from django.conf import settings
from forum.models import Post


class Follower(models.Model):
    the_followed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed')
    the_follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follower')
    time_followed = models.DateTimeField(auto_now_add=True)




# Create your models here.