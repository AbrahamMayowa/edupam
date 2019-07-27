from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from . models import Activities
from user.models import UserInfo


@login_required
def user_activities(request, user_id):
    get_user = get_object_or_404(UserInfo, pk=user_id)
    user = request.user
    if get_user != user:
        raise PermissionDenied('You are Forbidden!')
    else:
        get_user_notifications = Activities.objects.filter(performer=user).order_by('-created')
    context = {'get_user_notifications': get_user_notifications}
    return render(request, 'activity/user_activity.html', context)


# Create your views here.
