from . models import GeneralNotification, CommentNotification, ThumpedNotification, PersonalisedCommentNotif
from django.contrib.contenttypes.models import ContentType


# for following notification and other single entry activities
# check the author
def general_notification(user, target, action_string, author):
    general = GeneralNotification(performer=user, content_obj=target, content_type_author=author, \
        action_verb_general=action_string)
    general.save()

# in order to create abstraction for creating instance of personalised comment notifications
# check the below comment_notification function for it's implementation
def personalised_comment(notify_owner, related_notification_model, action):
        personal_comment_notification = PersonalisedCommentNotif(notification_owner=notify_owner, \
            related_comment_notification=related_notification_model, personal_action_verb=action)
        personal_comment_notification.save()




# it process personalise_comment function and save comment notification
def comment_notification(user, target_model, author):
    get_obj = ContentType.objects.get_for_model(target_model)
    existing_instance = CommentNotification.objects.filter(target_id=target_model.id, \
        target_comment_model=get_obj)
    if not existing_instance:
        comment_action = CommentNotification(content_obj=target_model, \
            model_author=author, comment_action_verb='commented')
        comment_action.save()
        comment_action.comment_performer_list.add(user)
        comment_action.save()
        for unique_user in comment_action.comment_performer_list.all():
            if unique_user != comment_action.model_author:
                personalised_comment(unique_user, comment_action, 'commented')
    else:
        for entry in existing_instance:
            if user not in entry.comment_performer_list.all():
                entry.comment_performer_list.add(user)
                entry.save()
                for user_obj in entry.comment_performer_list.all():
                    if user_obj != entry.model_author:
                        personalised_comment(user, entry, 'commented' )
        

def thumped_notification(target_model, author, action_user, action_string, comment_boolean):
    get_obj = ContentType.objects.get_for_model(target_model)
    # to check if the target model has already populated as model instance
    # if not it populated and if yes, the actor object on added to the MTM field
    get_notif = ThumpedNotification.objects.filter(target_id=target_model.id, thumped_target=get_obj)
    if not get_notif:
        thumped_notif = ThumpedNotification(content_obj=target_model, thumped_content_type_author=author, \
            thumped_action_string=action_string, is_comment_thump=comment_boolean)
        thumped_notif.save()
        thumped_notif.actor_list.add(action_user)
        thumped_notif.save()
    else:
        for entry in get_notif:
            if not action_user in entry.actor_list.all():
                entry.actor_list.add(action_user)
                entry.save()
                return True
            else:
                return False
        




        
        
