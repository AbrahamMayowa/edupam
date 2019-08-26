from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.db.models import Q


class JournalismManager(models.Manager):
    #to abstract general search queryset in the general_search app
    def search(self, query):
        qs = self.get_queryset()
        if query is not None:
            q_look = (Q(title__icontains=query)|
            Q(author__icontains=query))
            unique_qs = qs.filter(q_look).distinct()
        return unique_qs

class Journalism(models.Model):
    title = models.CharField(max_length=150)
    content = RichTextField()
    slug = models.SlugField(max_length=150, unique=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    number_of_views = models.IntegerField(default=0)
    claps = models.IntegerField(default=0)
    ranking_determination = models.IntegerField(default=0)
    hidden_status = models.BooleanField(default=False)
    objects = JournalismManager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('content_details', kwargs={'slug':self.slug, 'pk':self.id})
    
    def class_name(self):
        return self.__class__.__name__



    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class Comment(models.Model):
    comment_body = models.TextField(max_length=1000, blank=False, null=False)

    journalism = models.ForeignKey(Journalism, on_delete=models.CASCADE, related_name='journalisms')

    thump_up = models.ManyToManyField(settings.AUTH_USER_MODEL, \
        blank=True,related_name='user_upvote_comment')

    thump_down = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, \
        related_name='user_downvote_comment')

    comment_date = models.DateField(auto_now_add=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
        related_name='commment_creator')

    
    def class_name(self):
        return self.__class__.__name__
    