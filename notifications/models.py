from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from forum.models import Post, Comment

class GeneralNotification(models.Model):
    performer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='general_user_perfomers')
    content_type_general = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='general_target_model')
    content_type_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
        related_name='general_notification_author')
    object_id = models.PositiveIntegerField()
    content_obj = GenericForeignKey('content_type_general', 'object_id')
    action_verb_general = models.CharField(max_length=150, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    view_status = models.BooleanField(default=False)

    def class_name(self):
        return self.__class__.__name__


# only for the owner of the targeted model
class CommentNotification(models.Model):
    target_comment_model = models.ForeignKey(ContentType, related_name='comment_notification', on_delete=models.CASCADE)
    model_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
        related_name='post_author_notification')
    comment_performer_list = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='commentors')
    comment_action_verb = models.CharField(max_length=150, blank=False, null=False)
    target_id = models.PositiveIntegerField()
    content_obj = GenericForeignKey('target_comment_model', 'target_id')
    created = models.DateTimeField(auto_now_add=True)
    view_status = models.BooleanField(default=False)

    def class_name(self):
        return self.__class__.__name__


class PersonalisedCommentNotif(models.Model):
    notification_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
        related_name='personal_comment_notification')

    # to reference commentNotification perfomer_list manaytomany field and the target model
    related_comment_notification = models.ForeignKey(CommentNotification, \
        on_delete=models.CASCADE, related_name='commented_user')
    personal_action_verb = models.CharField(max_length=50, blank=False, null=False)

    view_status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def class_name(self):
        return self.__class__.__name__


# model obj for thumping of both post and comment and will only show to author of the post or comment
class ThumpedNotification(models.Model):
    # either post or comment
    thumped_target = models.ForeignKey(ContentType, on_delete=models.CASCADE, \
        related_name='thumped_up_target', blank=True, null=True)
    thumped_content_type_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, \
        related_name='models_author', db_index=True)
    actor_list = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='thumped_list')
    target_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    content_obj = GenericForeignKey('thumped_target', 'target_id')
    thumped_action_string = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    view_status = models.BooleanField(default=False)
    # this is for checking if instance's thumped_target is comment for easy rendering in the template
    is_comment_thump = models.BooleanField(default=False)

    def class_name(self):
        return self.__class__.__name__

    @property
    def contenttype_obj(self, obj):
        return ContentType.objects.get_for_model(self)



# Create your models here.
