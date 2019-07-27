from . models import Activities
from django.contrib.contenttypes.models import ContentType

def save_activity(user_id, target_model, action_sentence, action_boolean):
    # to prevent saving of dublicated actions by user on same related object id
    action = Activities(performer=user_id, content_object=target_model, action_verb=action_sentence, is_comment_thump=action_boolean)
    action.save()