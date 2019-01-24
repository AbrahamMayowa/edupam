from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import F
from django.http import Http404, HttpResponseRedirect
from django.db.models import Count
from user.models import UserInfo

from .forms import ContentForm
from .models import Journalism



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
            return redirect('content_details', pk=content_data.pk)
    else:
        form = ContentForm()
    return render(request, "cms/content_form.html", {'form': form})


# Editing content
@login_required(login_url='/user/login/')
def edit_content(request, pk):
    edit_form = get_object_or_404(Journalism, pk=pk)
    if request.user == edit_form.author:
        if request.method == 'POST':
            form = ContentForm(request.POST, instance=edit_form)
            if form.is_valid():
                new_data = form.save(commit=False)
                new_data.author = request.user
                new_data.published_data = timezone.now()
                new_data.save()
                return redirect('content_details', pk=new_data.pk)
        else:
            form = ContentForm(instance=edit_form)
        return render(request, 'cms/edit_content.html', {'form': form})


# content details view
def content_details(request, pk):
    try:
        content_data = Journalism.objects.get(pk=pk)
        content_data.number_of_views = F('number_of_views') + 1
        content_data.save()
    except Journalism.DoesNotExist:
        raise Http404('The page is not exist')
    context = {
        'content_data': content_data
    }
    return render(request, "cms/content_details.html", context)


# rendering the content curators main page
def content_main(request, pk):
    user_content = Journalism.objects.filter(pk=pk)


   # top_new_post = Journalism.objects.order_by('-published_date')[1:6]
    # top_viewed_post = Journalism.objects.annotate(click=Count('number_of_views')).order_by('-click')[:6]

    context = {'user_content': user_content

    }
    return render(request, 'cms/content_main.html', context)