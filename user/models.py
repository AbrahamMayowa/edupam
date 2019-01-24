from django.contrib.auth.models import AbstractUser

from django.db import models


class UserInfo(AbstractUser):
    school = models.CharField(max_length=100, blank=True, default='University of Ibadan')
    faculty = models.CharField(max_length=100, blank=True, default='Social Science')
    


# Create your models here.
