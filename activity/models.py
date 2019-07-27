from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Activities(models.Model):
    performer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
        related_name='user_perfomers')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, \
        related_name='activity_target_model')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    action_verb = models.CharField(max_length=150, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    is_comment_thump = models.BooleanField(default=False)



# Create your models here.
