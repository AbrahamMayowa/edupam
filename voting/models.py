from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Award(models.Model):
    organisation = models.CharField(max_length=200, blank=True, null=True)
    award_name = models.CharField(max_length=200)
    starting = models.DateField()
    vote_end = models.DateField()
    multiple_vote = models.BooleanField(default=True)

    def __str__(self):
        return self.award_name


class Category(models.Model):
    award = models.ForeignKey(Award, on_delete=models.CASCADE, related_name='awards')
    award_category = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.award_category


class Voters(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    the_voters = models.CharField(max_length=100)


class Contestant(models.Model):
    award_name = models.ForeignKey(Award, on_delete=models.CASCADE, related_name='contestant_awards')
    contestant_name = models.CharField(max_length=150, null=True, blank=True )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    vote = models.IntegerField()

    def number_of_vote(self):
        return Contestant.objects.filter(self.vote).count()
    vote_count = property(number_of_vote)








# Create your models here.
