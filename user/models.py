from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from follow.models import Follower


class UserInfo(AbstractUser):
    
    school = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=False, null=False)
    header_picture = models.ImageField(blank=True, upload_to='Profile_header', null=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='profile_picture')
    time_joined = models.DateTimeField(auto_now_add=True)
    user_follower = models.ManyToManyField('self', through=Follower, symmetrical=False, related_name='user_followers')


    # for image rendering
    @property
    def header_img_url(self):
        if self.header_picture:
            return self.header_picture.url
        else:
            return "/static/img/default_header.jpg"

    @property
    def profile_img_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return "/static/img/default_profile.png"

        

