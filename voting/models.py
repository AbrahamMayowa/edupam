from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.urls import reverse


class AwardManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            qs_look = (Q(organisation__icontains=query)|
            Q(award_name__icontains=query))
            unique_qs = qs.filter(qs_look).distinct()
        return unique_qs


class Award(models.Model):
    organisation = models.CharField(max_length=200, blank=True, null=True)
    award_name = models.CharField(max_length=200)
    starting = models.DateField()
    vote_end = models.DateField()
    multiple_vote = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = AwardManager()

    def __str__(self):
        return self.award_name

    def class_name(self):
        return self.__class__.__name__

    def get_absolute_url(self):
        return reverse('award_details', kwargs={'pk':pk})


class Category(models.Model):
    award = models.ForeignKey(Award, on_delete=models.CASCADE, related_name='awards')
    award_category = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.award_category


class Voters(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    the_voters = models.CharField(max_length=100)

class ContestantManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            qs_look = (Q(contestant_name__icontains=query))
            unique_qs = qs.filter(qs_look).distinct()
        return unique_qs

class Contestant(models.Model):
    award_name = models.ForeignKey(Award, on_delete=models.CASCADE, related_name='contestant_awards')
    contestant_name = models.CharField(max_length=150, null=True, blank=True )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    vote = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    objects = ContestantManager()

    def class_name(self):
        return self.__class__.__name__

    def number_of_vote(self):
        return Contestant.objects.filter(self.vote).count()
    vote_count = property(number_of_vote)

    








# Create your models here.
