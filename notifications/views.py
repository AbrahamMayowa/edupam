from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from . models import CommentNotification, PersonalisedCommentNotif, \
    ThumpedNotification, GeneralNotification
from user.models import UserInfo
from itertools import chain
from operator import attrgetter

def update_view_status(request, user_id):
    user = request.user
    get_user = get_object_or_404(UserInfo, pk=user_id)
    if request.user != get_user:
        raise PermissionDenied('Permission Denied! Sorry!')
    comments = CommentNotification.objects.filter(model_author=user)
    general = GeneralNotification.objects.filter(performer=user)
    personal_comment = PersonalisedCommentNotif.objects.filter(notification_owner=user)
    thumped_notif = ThumpedNotification.objects.filter(thumped_content_type_author=user)
    all_query = sorted(chain(comments, general, personal_comment, thumped_notif), key=attrgetter('created'), reverse=True)

    # update view status to true when user has made request or view it
    for entry in all_query:
        entry.view_status = True
        entry.save()
    context = {'all_query': all_query}
    return render(request, 'notifications/user_notifications.html', context)

# Create your views here.
