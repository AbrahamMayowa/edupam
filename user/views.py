from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserForm, ChangeUser, ProfilePictureForm, ProfileHeaderForm
from .models import UserInfo
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse



def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user_pk = form.save(commit=False)
            user_pk.save()
            return redirect('welcome', user_pk.id)
    else:
        form = UserForm()
    context = {'form':form}
    return render(request, 'user/signup.html', context)

#user updating view
@login_required
def update_user_info(request, pk):
    get_user = get_object_or_404(UserInfo, pk=pk)
    user = request.user
    if user != get_user:
        raise PermissionDenied('You are not allowed')
    if request.method == 'POST':
        form = ChangeUser(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been successfully updated')
            return redirect('user_info', get_user.pk)
    else:
        form = ChangeUser(request.POST, instance=user)
    context = {'form':form}
    return render(request, 'user/user_profile_update.html', context)

# upload user profile picture
@login_required
def upload_profile_picture(request, pk):
    get_user = get_object_or_404(UserInfo, pk=pk)
    user = request.user
    if user != get_user:
        raise PermissionDenied('Permission Denied')
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile picture updated!')
            return redirect('user_info', get_user.pk)
    else:
        form = ProfilePictureForm(instance=user)
    context = {'form': form}
    return render(request, 'user/user_info.html', context)


#upload user profile header
@login_required
def upload_header_picture(request, pk):
    get_user = get_object_or_404(UserInfo, pk=pk)
    user = request.user
    if user != get_user:
        raise PermissionDenied('Permission Denied')
    if request.method == 'POST':
        form = ProfileHeaderForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Header picture added!')
            return redirect('user_info', get_user.pk)
    else:
        form = ProfileHeaderForm(instance=user)
    context = {'header_form': form}
    return render(request, 'user/user_info.html', context)

#user profile
def user_profile(request, pk):
    header_form = ProfileHeaderForm()
    form = ProfilePictureForm()
    user = get_object_or_404(UserInfo, pk=pk)
    context = {'user_info':user,
    'header_form':header_form,
    'form':form}
    return render(request, 'user/user_info.html', context)

#welcome view, migth add more info
def welcome_page(request, pk):
    new_user = get_object_or_404(UserInfo, pk=pk)
    context = {'new_user':new_user}
    return  render(request, 'user/welcome.html', context)



