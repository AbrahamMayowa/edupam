from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import F
from django.http import Http404, HttpResponseRedirect
from django.db.models import Count
from user.models import UserInfo
from django.core.exceptions import PermissionDenied

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

def delete_content(request, slug, pk):
    deleting_content = get_object_or_404(Journalism, pk=pk, slug=slug)
    if request.user == deleting_content.author:
        deleting_content.delete()
    else:
        raise PermissionDenied('Permision denied')

    return redirect('curator_profile', content_id=deleting_content.pk)



# content details view
def content_details(request, pk, slug):
    try:
        content_data = Journalism.objects.get(slug=slug, pk=pk)
        content_data.number_of_views = F('number_of_views') + 1
        content_data.save()
    except Journalism.DoesNotExist:
        raise Http404('The page is not exist')
    context = {
        'content_data': content_data
    }
    return render(request, "cms/content_details.html", context)


# rendering the content curators main page
def content_creator_profile(request, content_id):
    received_pk = Journalism.objects.get(pk=content_id)
    all_profile_content = Journalism.objects.filter(author=received_pk.author)

    # top_viewed_post = Journalism.objects.annotate(click=Count('number_of_views')).order_by('-click')[:6]

    context = {'all_profile_content': all_profile_content,}
    
    return render(request, 'cms/curator_page.html', context)


def main_page(request):
    all_content = Journalism.objects.all().order_by('-draft_date')[:10]
    ranking = Journalism.objects.all().order_by('-ranking_determination').filter(post_status='p').exlude(report__isnull=False)

    context = {'all_content':all_content, 'ranking': ranking}
    return render(request, 'cms/content_main.html', context)


@login_required
def comment_view(request, pk):
    journalism_pk = get_object_or_404(Journalism, pk=pk)
    if request.method == 'POST':
        form2 = CommentForm(request.POST)
        if form2.is_valid():
            form_data = form2.save(commit=False)
            form_data.content = journalism_pk
            form_data.comment_date = timezone.now()
            form_data.comment_author = request.user
            form_data.save()
            return redirect('content_details', pk=journalism_pk.pk, slug=journalism_pk.slug)
    else:
        form2 = CommentForm()
    return render(request, 'cms/content_details.html', {'form2':form2})

@login_required
def edit_comment(request, comment_id, slug, journalist_id):
    journalist_data = get_object_or_404(Journalism, journalist_id=journalist_id, slug=slug)
    comment_instance = get_object_or_404(Comment, comment_id=comment_id)
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
        'comment_form_instance': comment_form_instance    }
    return render(request, 'cms/content_details.html', context)


def delete_comment(request, pk, journalist_id):
    journalism = get_object_or_404(Journalism, journalist_id=journalist_id)
    deleted_comment = get_object_or_404(Comment, pk=pk)
    if request.user == deleted_comment.comment_author or request.user == journalism.author:
        deleted_comment.delete()
    else:
        raise PermissionDenied('Permission denial')
    return redirect('content_details', pk=journalism.pk, slug=journalism.slug)


@login_required
def replycomment(request, comment_id, content_id, slug):
    



def clap(request, pk, slug):
    data = Journalism.objects.get(pk=pk)
    data.claps = F('claps') + 1
    data.save()
    return redirect('content_details', pk=data.pk, slug=data.slug )


def comment_thump_up(request, pk, slug):
    content = get_object_or_404(Journalism, pk=pk, slug=slug)
    comment = get_object_or_404(Comment, pk=pk)


def to_publish(request, pk):
    content = get_object_or_404(Journalism, pk=pk)
    content.publish()
    return redirect('content_details', pk=content.pk)




    







