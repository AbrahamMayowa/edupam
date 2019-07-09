from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

class Journalism(models.Model):

    title = models.CharField(max_length=150)
    content = RichTextUploadingField()
    slug = models.SlugField(max_length=150, unique=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    draft_date = models.DateTimeField(auto_now_add=True)
    number_of_views = models.IntegerField(default=0)
    claps = models.IntegerField(default=0)
    ranking_determination = models.IntegerField(default=0)


    def __str__(self):
        return self.title



    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)



class Comment(models.Model):
    comment_body = models.CharField(max_length=1000, blank=False, null=False)
    journalism = models.ForeignKey(Journalism, on_delete=models.CASCADE, related_name='journalisms')
    thump_up = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,related_name='user_upvote_comment')
    thump_down = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_downvote_comment')
    comment_date = models.DateField(auto_now_add=True)
    comment_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commment_creator')
    










    


        
    
        


# Create your models here.
