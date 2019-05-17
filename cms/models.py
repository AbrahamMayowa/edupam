from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

class Journalism(models.Model):

    PUBLISH_STATUS = (
        ('p', 'Publish'),
        ('d', 'Draft'),
    )

    title = models.CharField(max_length=150)
    content = RichTextUploadingField()
    slug = models.SlugField(max_length=150, unique=False)
    published_date = models.DateField(timezone.now(), blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    draft_date = models.DateTimeField()
    number_of_views = models.PositiveIntegerField(default=0)
    post_status = models.CharField(max_length=1, choices=PUBLISH_STATUS, null=True, blank=True, default='d')
    claps = models.PositiveIntegerField(default=0, null=True, blank=True)


    def __str__(self):
        return self.title

    def publish(self):
        self.post_status = 'p'
        self.published_date = timezone.now()
        self.save()

    def draft(self):
        self.post_status = 'd'
        self.published_date = None
        self.draft_date = timezone.now()
        self.save()


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.post_status =  'p':
            self.published_date = timezone.now()    
        super().save(*args, **kwargs)

    
    def calculate_ranking_algorithm(self):
        clap_value = 60/100 * self.claps
        view_value = 40/100 * self.number_of_views

        return round(clap_value + view_value)

    ranking_determination = property(calculate_ranking_algorithm)



class Comment(models.Model):
    comment_body = models.CharField(max_length=1000, blank=False, null=False)
    content = models.ForeignKey(Journalism, on_delete=models.CASCADE, related_name='journalisms')
    thump_up = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True)
    thump_down = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True)
    comment_date = models.DateField()
    comment_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comment')

class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_reply')
    reply = models.CharField(max_length=1000)
    respondent = models.ManyToManyField(settings.AUTH_USER_MODEL)
    










    


        
    
        


# Create your models here.
