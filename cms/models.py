from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class Journalism(models.Model):
    title = models.CharField(max_length=150)
    content = RichTextUploadingField(blank=False, null=False)
    slug = models.SlugField(max_length=150, unique=False)
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='journalisms')
    draft_date = models.DateTimeField(auto_now_add=True)
    number_of_views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def _unique_slug(self):
        self.slug = slugify(self.title)
        super(Journalism, self).save()


# Create your models here.
