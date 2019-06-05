from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import F
from django.http import Http404, HttpResponseRedirect
from django.db.models import Count
from user.models import UserInfo
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.template.loader import render_to_string
from collections import defaultdict

from .forms import ContentForm, CommentForm
from .models import Journalism, Comment


# content form
@login_required(login_url='/user/login/')
def content_view(request):
    if request.method == 'POST':
        form = ContentForm(request.POST)
        if form.is_valid():
            content_data = form.save(commit=False)
            content_data.author = request.user
            content_data.published_date = timezone.now()
            content_data.save()

            return redirect('content_details', pk=content_data.pk, slug=content_data.slug)
    else:
        form = ContentForm()
    return render(request, "cms/content_form.html", {'form': form})


# Editing content
@login_required(login_url='/user/login/')
def edit_content(request, pk, slug):
    edit_form = get_object_or_404(Journalism, pk=pk, slug=slug)
    if request.user != edit_form.author:
        raise PermissionDenied("You can edit another's user content")
    elif request.method == 'POST':
        form = ContentForm(request.POST, instance=edit_form)
        if form.is_valid():
            new_data = form.save(commit=False)
            new_data.author = request.user
            new_data.published_data = timezone.now()
            new_data.save()
            return redirect('content_details', pk=new_data.pk, slug=new_data.slug)
    else:
        form = ContentForm(instance=edit_form)
    return render(request, 'cms/edit_content.html', {'form': form})


#view to process removal of content
@login_required
def delete_content(request, pk):
    delete_content = get_object_or_404(Journalism, pk=pk)

    if request.user  == delete_content.author:
        delete_content.delete()
    else:
        raise PermissionDenied('Permision denied')

    return redirect('main_page')

# this view redirect to a page to confirm deleting content
def redirect_delete(request, pk):
    getting_object = get_object_or_404(Journalism, pk=pk)
    context = {
        'getting_object':getting_object,
    }
    return render(request, 'cms/confirm_delete.html', context)







# content details view
def content_details(request, pk, slug):
    form = CommentForm()
    try:
        content_data = Journalism.objects.get(slug=slug, pk=pk)
        content_data.number_of_views = F('number_of_views') + 1
        content_data.save()
    except Journalism.DoesNotExist:
        raise Http404('The page is not exist')
    comment_list = content_data.journalisms.all()
    context = {
        'content_data': content_data, 'comment_list': comment_list, 'form':form, 
    }
    return render(request, "cms/content_details.html", context)


# rendering the content curators main page
def content_creator_profile(request, pk):
    received_pk = Journalism.objects.get(pk=pk)
    all_profile_content = Journalism.objects.filter(author=received_pk.author)

    # top_viewed_post = Journalism.objects.annotate(click=Count('number_of_views')).order_by('-click')[:6]

    context = {'all_profile_content': all_profile_content,}
    
    return render(request, 'cms/curator_page.html', context)

#quary object for the main page and dynamic calculation of list ranking(ranking_determination)
def main_page(request):
    journalism_object = Journalism.objects.all()   
    for single_object in journalism_object:
        clap_value = 60/100 * single_object.claps
        view_value = 40/100 * single_object.number_of_views
        total_sum = round(clap_value + view_value)
        single_object.ranking_determination = total_sum
    all_content = journalism_object.order_by('-draft_date')[:3]
    determing_query = journalism_object.order_by('-ranking_determination')
    ranking = determing_query.difference(all_content)

    context = {'all_content':all_content, 'ranking': ranking}
    return render(request, 'cms/content_main.html', context)




@login_required
def comment_view(request, pk):
    journalism_pk = get_object_or_404(Journalism, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.journalism = journalism_pk
            form_data.comment_date = timezone.now()
            form_data.comment_author = request.user
            form_data.save()
            return redirect('content_details', pk=journalism_pk.id, slug=journalism_pk.slug)     
    else:
        form = CommentForm()
    return render(request, 'cms/content_details.html', {'form':form})



@login_required
def edit_comment(request, comment_id, journalist_id):
    journalist_data = get_object_or_404(Journalism, pk=journalist_id)
    comment_instance = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment_instance.comment_author or request.user != journalist_data.author:
        raise PermissionDenied('You are forbidden from editing this comment')
    elif request.method == 'POST':
        comment_form_instance = CommentForm(request.POST, instance=comment_instance)
        if comment_form_instance.is_valid():
            form_data = comment_form_instance.save(commit=False)
            form_data.content = journalist_data
            form_data.comment_date = timezone.now()
            form_data.comment_author = request.user
            form_data.save()
            return redirect('content_details', pk=journalist_data.pk, slug=journalist_data.slug)
    else:
        comment_form_instance = CommentForm(instance=comment_instance)

    context = {
        'journalist_data': journalist_data, 
        'form': comment_form_instance,
        'comment_instance': comment_instance }
    return render(request, 'cms/delete_and_edit_comment.html', context)

# i will need to write message framework here
def delete_comment(request, comment_pk, journalist_id):
    journalism = get_object_or_404(Journalism, journalist_id=pk)
    deleted_comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == deleted_comment.comment_author or request.user == journalism.author:
        deleted_comment.delete()
    else:
        raise PermissionDenied('Permission denial')
    return redirect('content_details', pk=journalism.pk, slug=journalism.slug)



"""
@login_required
def replycomment(request, comment_id, content_id, slug):

"""
    


@login_required
def clap(request, pk):
    data = {}
    try:
        content = Journalism.objects.get(pk=pk)
        content.claps = F('claps') + 1
        content.save()
        data['successful'] = True
        ajax_query = Journalism.objects.get(pk=pk)
        data['clap_numb'] = ajax_query.claps
    except Journalism.DoesNotExist:
        data['successful'] = False
    return JsonResponse(data)



@login_required
def comment_thump_up(request, pk):
    data ={}
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user
    if user not in comment.thump_up.all():
        if user not in comment.thump_down.all():
            comment.thump_up.add(user)
            data['thumped_up'] = True
    elif user not in comment.thump_up.all() and user in comment.thump_down.all():
        comment.thump_down.remove(user)
        comment.thump_up.add(user)
        data['thumped_up'] = True
    elif user in comment.thump_up.all():
        comment.thump_up.remove(user)
        data['thumped_up'] = False

    numb_of_thump_up = get_object_or_404(Comment, pk=pk)
    data['thump_up_count'] = numb_of_thump_up.thump_up.count()
    data['thump_up_count'] =numb_of_thump_up.thump_down.count()
    return JsonResponse(data)

@login_required
def comment_thump_down(request, pk):
    data ={}
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user
    if user not in comment.thump_down.all():
        if user not in comment.thump_up.all():
            comment.thump_down.add(user)
            data['thumped_down'] = True
    elif user not in comment.thump_down.all() and user in comment.thump_up.all():
        comment.thump_up.remove(user)
        comment.thump_down.add(user)
        data['thumped_down'] = True
    elif user in comment.thump_down.all():
        comment.thump_down.remove(user)
        data['thumped_down'] = False

    numb_of_thump_down = get_object_or_404(Comment, pk=pk)
    data['thump_down_count'] = numb_of_thump_down.thump_down.count()
    data['thump_up_count'] = numb_of_thump_down.thump_up.count()
    return JsonResponse(data)



        





    







