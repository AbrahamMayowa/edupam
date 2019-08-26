from django.db.models.signals import post_save
from django.dispatch import	receiver
from . models import Post
from . models import Comment
from . models import CommentReply


@receiver(post_save, sender=Post.user_array_flag_post)
def post_flag_signal(sender, instance, **kwargs):
    if instance.user_array_flag_post.count() >= 20:
        instance.post_hidden = True
        instance.save()

# flagging comment hidden
@receiver(post_save, sender=Comment.user_array_flag_comment)
def comment_flag_off(sender, instance, **kwargs):
    if instance.user_array_flag_comment.count() >= 20:
        instance.comment_hidden = True
        instance.save()

@receiver(post_save, sender=CommentReply.user_array_flag_comment_reply)
def comment_reply_flag_off(sender, instance, **kwargs):
    if instance.user_array_flag_comment_reply.count() >= 20:
        instance.comment_reply_hidden = True
        instance.save()