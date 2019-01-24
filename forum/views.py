from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms import modelformset_factory
from django.template import RequestContext
from django.contrib import messages
from django.db.models import F, Count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from itertools import chain

from .forms import PostForm, CommentForm, PictureForm
from .models import Post, Picture


# view for uploading of new post. It has formset for uploading multiple images of the post
@login_required(login_url='/user/login/')
def post_form_view(request):
    ImageFormSet = modelformset_factory(Picture, fields=('image',), extra=3)
    if request.method == "POST":
        form = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Picture.objects.none())
# validating both postform and pictureform
        if form.is_valid() and formset.is_valid():
            # saving post to the db
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # saving formset
            for form_entry in formset:
                try:
                    photo = Picture(post=post, image=form_entry.cleaned_data['image'])
                    photo.save()
                except Exception as e:
                    break
            return redirect('post_details', pk=post.pk)
    else:
        form = PostForm()
        formset = ImageFormSet(queryset=Picture.objects.none())
    context = {
        'form': form,
        'formset': formset
    }
    return render(request, "forum/post_forum.html", context)


# post comment view
def post_comment_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, request.File)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.published_date = timezone.now()
            comment.save()
            return redirect('post_details', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, "forum/post_details.html", {'form': form})


# for rendering post details which also save the number of which the object pk is viewed
def post_details(request, pk):
    try:
        post_list = get_object_or_404(Post, pk=pk)
        post_list.view_number = F('view_number') + 1
        post_list.save()
    except Post.DoesNotExist:
        raise Http404('The page is not exist')
    context = {
        'post_list': post_list
    }
    return render(request, "forum/post_details.html", context)






def academic_post_view(request):
    # queryset top 5 of the most viewed post
    academic_popular = Post.objects.filter(category='academic').annotate(number_of_click=Count('view_number')).order_by(
        '-number_of_click')[:6]
    # show top 20 of the new post entry
    academic_newest = Post.objects.filter(category='academic').order_by('-published_date')[1:20]
    # queryset 7 to 15 of the most viewed post
    academic_popular2 = Post.objects.filter(category='academic').annotate(clicks=Count('view_number')).order_by('-clicks')[7:15]
    # top 21 to 200 of the newest post
    academic_newest2 = Post.objects.filter(category='academic').order_by('-published_date')[21:200]
    # chain the queryset
    academic_list = list(chain(academic_popular, academic_newest, academic_popular2, academic_newest2))
    paginator = Paginator(academic_list, 15)
    page = request.GET.get('page')
    academic_posts = paginator.get_page(page)
    return render(request, 'forum/academic_post.html', {'posts': academic_posts})


# algorithm for showing opportunity post
def opportunity_post_view(request):
    # filtering post relating to opportunity and displaying only top 5 objects with highest views
    opportunity_popular = Post.objects.filter(category='opportunity').annotate(number_of_click=Count('view_number')).order_by(
        '-number_of_click')[:6]
    # show top 20 of the new post entry
    opportunity_newest = Post.objects.filter(category='opportunity').order_by('-published_date')[1:20]
    # queryset 7 to 15 of the most viewed post
    opportunity_popular2 = Post.objects.filter(category='opportunity').annotate(clicks=Count('view_number')).order_by(
        '-clicks')[7:15]
    # top 21 to 200 of the newest post
    opportunity_newest2 = Post.objects.filter(category='opportunity').order_by('-published_date')[21:200]
    # chain the queryset
    opportunity_list = list(chain(opportunity_popular, opportunity_newest, opportunity_popular2, opportunity_newest2))
    paginator = Paginator(opportunity_list, 15)
    page = request.GET.get('page')
    opportunity_posts = paginator.get_page(page)
    return render(request, 'forum/opportunity_post.html', {'opportunity_posts': opportunity_posts})



# Algorithm for rendering of business hub related post
def business_hub_view(request):
    # filtering post relating to business hub and displaying only top 5 objects with highest views
    business_popular = Post.objects.filter(category='business_hub').annotate(
        number_of_click=Count('view_number')).order_by(
        '-number_of_click')[:6]
    # show top 20 of the new post entry
    business_newest = Post.objects.filter(category='business_hub').order_by('-published_date')[1:20]
    # queryset 7 to 15 of the most viewed post
    business_popular2 = Post.objects.filter(category='business_hub').annotate(clicks=Count('view_number')).order_by(
        '-clicks')[7:15]
    # top 21 to 200 of the newest post
    business_newest2 = Post.objects.filter(category='business_hub').order_by('-published_date')[21:200]
    # chain the queryset
    business_list = list(chain(business_popular, business_newest, business_popular2, business_newest2))
    paginator = Paginator(business_list, 15)
    page = request.GET.get('page')
    business_posts = paginator.get_page(page)
    return render(request, 'forum/business_post.html', {'business_posts': business_posts})


# Algorithm for rendering of admission related post
def admission_view(request):
    # filtering post relating to business hub and displaying only top 5 objects with highest views
    admission_popular = Post.objects.filter(category='admission').annotate(
        number_of_click=Count('view_number')).order_by(
        '-number_of_click')[:6]
    # show top 20 of the new post entry
    admission_newest = Post.objects.filter(category='admission').order_by('-published_date')[1:20]
    # queryset 7 to 15 of the most viewed post
    admission_popular2 = Post.objects.filter(category='admission').annotate(clicks=Count('view_number')).order_by(
        '-clicks')[7:15]
    # top 21 to 200 of the newest post
    admission_newest2 = Post.objects.filter(category='admission').order_by('-published_date')[21:200]
    # chain the queryset
    admission_list = list(chain(admission_popular, admission_newest, admission_popular2, admission_newest2))
    paginator = Paginator(admission_list, 15)
    page = request.GET.get('page')
    admission_posts = paginator.get_page(page)
    return render(request, 'forum/admission_post.html', {'admission_posts': admission_posts})


# Algorithm for rendering of events related post
def events_view(request):
    # filtering post relating to events and displaying only top 5 objects with highest views
    events_popular = Post.objects.filter(category='events').annotate(
        number_of_click=Count('view_number')).order_by(
        '-number_of_click')[:6]
    # show top 20 of the new post entry
    events_newest = Post.objects.filter(category='events').order_by('-published_date')[1:20]
    # queryset 7 to 15 of the most viewed post
    events_popular2 = Post.objects.filter(category='events').annotate(clicks=Count('view_number')).order_by(
        '-clicks')[7:15]
    # top 21 to 200 of the newest post
    events_newest2 = Post.objects.filter(category='events').order_by('-published_date')[21:200]
    # chain the queryset
    events_list = list(chain(events_popular, events_newest, events_popular2, events_newest2))
    paginator = Paginator(events_list, 15)
    page = request.GET.get('page')
    events_posts = paginator.get_page(page)
    return render(request, 'forum/events_post.html', {'events_posts': events_posts})


# Algorithm for rendering of politics related post
def politics_view(request):
    # filtering post relating to politics and displaying only top 5 objects with highest views
    politics_popular = Post.objects.filter(category='politics').annotate(
        number_of_click=Count('view_number')).order_by(
        '-number_of_click')[:6]
    # show top 20 of the new post entry
    politics_newest = Post.objects.filter(category='politics').order_by('-published_date')[1:20]
    # queryset 7 to 15 of the most viewed post
    politics_popular2 = Post.objects.filter(category='politics').annotate(clicks=Count('view_number')).order_by(
        '-clicks')[7:15]
    # top 21 to 200 of the newest post
    politics_newest2 = Post.objects.filter(category='politics').order_by('-published_date')[21:200]
    # chain the queryset
    politics_list = list(chain(politics_popular, politics_newest, politics_popular2, politics_newest2))
    paginator = Paginator(politics_list, 15)
    page = request.GET.get('page')
    politics_posts = paginator.get_page(page)
    return render(request, 'forum/politics_post.html', {'politics_posts': politics_posts})


# Algorithm for rendering of award related post
def award_view(request):
    # filtering post relating to award and displaying only top 5 objects with highest views
    award_popular = Post.objects.filter(category='award').annotate(
        number_of_click=Count('view_number')).order_by(
        '-number_of_click')[:6]
    # show top 20 of the new post entry
    award_newest = Post.objects.filter(category='award').order_by('-published_date')[1:20]
    # queryset 7 to 15 of the most viewed post
    award_popular2 = Post.objects.filter(category='award').annotate(clicks=Count('view_number')).order_by(
        '-clicks')[7:15]
    # top 21 to 200 of the newest post
    award_newest2 = Post.objects.filter(category='award').order_by('-published_date')[21:200]
    # chain the queryset
    award_list = list(chain(award_popular, award_newest, award_popular2, award_newest2))
    paginator = Paginator(award_list, 15)
    page = request.GET.get('page')
    award_posts = paginator.get_page(page)
    return render(request, 'forum/award_post.html', {'award_posts': award_posts})


# Algorithm for rendering of relationship related post
def relationship_view(request):
    # filtering post relating to relationship and displaying only top 5 objects with highest views
    relationship_popular = Post.objects.filter(category='relationship').annotate(
        number_of_click=Count('view_number')).order_by(
        '-number_of_click')[:6]
    # show top 20 of the new post entry
    relationship_newest = Post.objects.filter(category='relationship').order_by('-published_date')[1:20]
    # queryset 7 to 15 of the most viewed post
    relationship_popular2 = Post.objects.filter(category='relationship').annotate(clicks=Count('view_number')).order_by(
        '-clicks')[7:15]
    # top 21 to 200 of the newest post
    relationship_newest2 = Post.objects.filter(category='relationship').order_by('-published_date')[21:200]
    # chain the queryset
    relationship_list = list(chain(relationship_popular, relationship_newest, relationship_popular2, relationship_newest2))
    paginator = Paginator(relationship_list, 15)
    page = request.GET.get('page')
    relationship_posts = paginator.get_page(page)
    return render(request, 'forum/relationship_post.html', {'relationship_posts': relationship_posts})


# Algorithm for rendering of knowledge related post
def knowledge_view(request):
    # filtering post relating to knowledge and displaying only top 5 objects with highest views
    knowledge_popular = Post.objects.filter(category='knowledge').annotate(
        number_of_click=Count('view_number')).order_by(
        '-number_of_click')[:6]
    # show top 20 of the new post entry
    knowledge_newest = Post.objects.filter(category='knowledge').order_by('-published_date')[1:20]
    # queryset 7 to 15 of the most viewed post
    knowledge_popular2 = Post.objects.filter(category='knowledge').annotate(clicks=Count('view_number')).order_by(
        '-clicks')[7:15]
    # top 21 to 200 of the newest post
    knowledge_newest2 = Post.objects.filter(category='knowledge').order_by('-published_date')[21:200]
    # chain the queryset
    knowledge_list = list(chain(knowledge_popular, knowledge_newest, knowledge_popular2, knowledge_newest2))
    paginator = Paginator(knowledge_list, 15)
    page = request.GET.get('page')
    knowledge_posts = paginator.get_page(page)
    return render(request, 'forum/knowledge_post.html', {'knowledge_posts': knowledge_posts})


# Algorithm for rendering of creative_writing related post
def creative_writing_view(request):
    # filtering post relating to knowledge and displaying only top 5 objects with highest views
    creative_writing_popular = Post.objects.filter(category='creative_writing').annotate(
        number_of_click=Count('view_number')).order_by(
        '-number_of_click')[:6]
    # show top 20 of the new post entry
    creative_writing_newest = Post.objects.filter(category='creative_writing').order_by('-published_date')[1:20]
    # queryset 7 to 15 of the most viewed post
    creative_writing_popular2 = Post.objects.filter(category='creative_writing').annotate(clicks=Count('view_number')).order_by(
        '-clicks')[7:15]
    # top 21 to 200 of the newest post
    creative_writing_newest2 = Post.objects.filter(category='creative_writing').order_by('-published_date')[21:200]
    # chain the queryset
    creative_writing_list = list(chain(creative_writing_popular, creative_writing_newest, creative_writing_popular2, creative_writing_newest2))
    paginator = Paginator(creative_writing_list, 15)
    page = request.GET.get('page')
    creative_writing_posts = paginator.get_page(page)
    return render(request, 'forum/creative_writing_post.html', {'creative_writing_posts': creative_writing_posts})


# Algorithm for rendering of general related post
def general_view(request):
    # filtering post relating to knowledge and displaying only top 5 objects with highest views
    general_popular = Post.objects.filter(category='general').annotate(
        number_of_click=Count('view_number')).order_by(
        '-number_of_click')[:6]
    # show top 20 of the new post entry
    general_newest = Post.objects.filter(category='general').order_by('-published_date')[1:20]
    # queryset 7 to 15 of the most viewed post
    general_popular2 = Post.objects.filter(category='general').annotate(clicks=Count('view_number')).order_by(
        '-clicks')[7:15]
    # top 21 to 200 of the newest post
    general_newest2 = Post.objects.filter(category='general').order_by('-published_date')[21:200]
    # chain the queryset
    general_list = list(chain(general_popular, general_newest, general_popular2, general_newest2))
    paginator = Paginator(general_list, 15)
    page = request.GET.get('page')
    general_posts = paginator.get_page(page)
    return render(request, 'forum/general_post.html', {'general_posts': general_posts})

























