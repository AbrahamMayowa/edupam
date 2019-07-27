from django.shortcuts import render
from user.models import UserInfo
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Follower
from forum.models import Post
from django.contrib.auth.decorators import login_required
from notifications.utils import general_notification


#to follow a user
@login_required
def	user_follow(request, pk):
	user = request.user
	get_user = get_object_or_404(UserInfo, pk=pk)
	data = {}
	if user not in get_user.user_followers.all():
		Follower.objects.get_or_create(the_followed=get_user, the_follower=user)
		general_notification(user, get_user, 'following', get_user)

		data['follower_add'] = True
	else:
		Follower.objects.filter(the_followed=get_user, the_follower=user).delete()
		data['follower_add'] = False
	return JsonResponse(data)


		


	