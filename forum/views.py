from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms import formset_factory, inlineformset_factory
from django.template import RequestContext
from django.contrib import messages
from django.db.models import F, Count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from itertools import chain
from django.core.exceptions import PermissionDenied

from general_search.forms import SearchForm
from .forms import PostForm, CommentForm, PictureForm, CommentPictureForm, ReplyForm
from .models import Post, Picture, CommentPicture, Comment, CommentReply
from activity.utils import save_activity
from notifications.utils import general_notification, comment_notification, thumped_notification


# view for uploading of new post. It has formset for uploading multiple images of the post
@login_required
def post_form_view(request):
    ImageFormSet = formset_factory(PictureForm, extra=3)
    user = request.user
    if request.method == "POST":
        form = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)
# validating both postform and pictureform
        if form.is_valid() and formset.is_valid():
            # saving post to the db
            post = form.save(commit=False)
            post.author = user
            post.save()
            # saving formset
            for form_entry in formset:
                data = form_entry.save(commit=False)
                data.post = post
                data.save()
                save_activity(user, post, 'created a thread', False)
                return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostForm()
        formset = ImageFormSet()
    context = {
        'form': form,
        'formset': formset
    }
    return render(request, "forum/post_form_and_list.html", context)


def post_list_and_post_create_form(request):
    all_newest = Post.objects.all().exclude(post_hidden=True).order_by('-created')
    form = PostForm()
    search_form = SearchForm()
    ImageFormSet = formset_factory(PictureForm, extra=3)
    formset = ImageFormSet()
    context = {
        'posts': all_newest,
        'form': form,
        'formset': formset,
        'search_form': search_form,
    }
    return render(request, 'forum/post_form_and_list.html', context)

@login_required
def follow_post(request, post_id):
    get_post = get_object_or_404(Post, pk=post_id)
    user = request.user
    data = {}
    if user not in get_post.user_followed.all():
        get_post.user_followed.add(user)
        save_activity(user, get_post, 'following', False)
        data['added'] = True
    else:
        get_post.user_followed.remove(user)
        data['added'] = False
    return JsonResponse(data)


# let user know if he or she has already flaged the post in the template and bootstrap model for this
@login_required
def post_flag_redirect(request, post_id):
    get_post = get_object_or_404(Post, pk=post_id)
    context = {
        'get_post': get_post,
    }
    return render(request, 'forum/post_flag_redirect.html', context)


# the main post flagging is done through this ajax request
@login_required
def post_flag_ajax(request, post_id):
    data = {}
    user = request.user
    get_post = get_object_or_404(Post, pk=post_id)
    if user in get_post.user_array_flag_post.all():
        data['flag'] = False
    get_post.user_array_flag_post.add(user)
    data['flag'] = True
    return JsonResponse(data)



@login_required
def edit_post(request, post_id):
    get_post = get_object_or_404(Post, pk=post_id)
    ImageFormset = inlineformset_factory(Post, Picture, fields=('image',))
    if request.user != get_post.author:
        raise PermissionDenied('You are Forbidden')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=get_post)
        formset = ImageFormset(request.POST, request.FILES, instance=get_post)
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            for form_data in formset:
                data = form_data.save(commit=False)
                data.post = get_post
                data.save()
                return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostForm(instance=get_post)
        formset = ImageFormset(instance=get_post)
    context = {
        'form':form,
        'formset': formset
    }

    return render(request, 'forum/edit_post.html', context)

# thumping up post
@login_required
def post_thumped_up(request, post_id):
    user = request.user
    data = {}
    get_post = get_object_or_404(Post, pk=post_id)
    if user not in get_post.post_thumped_up.all():
        get_post.post_thumped_up.add(user)
        data['added'] = True
        save_activity(user, get_post, 'thumped up', False)
        thumped_notification(get_post, get_post.author, user, 'thumped up', False)
        if user in get_post.post_thumped_down.all():
            get_post.post_thumped_down.remove(user)
            data['already_thumped_down'] = True
    else:
        get_post.post_thumped_up.remove(user)
        data['added'] = False
    return JsonResponse(data)


# thumping down post
@login_required
def post_thumped_down(request, post_id):
    user = request.user
    data = {}
    get_post = get_object_or_404(Post, pk=post_id)
    if user not in get_post.post_thumped_down.all():
        get_post.post_thumped_down.add(user)
        save_activity(user, get_post, 'thumped down', False)
        thumped_notification(get_post, get_post.author, user, 'thumped down', False)
        data['added'] = True
        if user in get_post.post_thumped_up.all():
            get_post.post_thumped_up.remove(user)
            data['already_thumped_up'] = True
    else:
        get_post.post_thumped_down.remove(user)
        data['added'] = False
    return JsonResponse(data)


# post comment view
@login_required
def post_comment_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    CommentPictureFormset = formset_factory(CommentPictureForm, extra=3)
    if request.method == "POST":
        form = CommentForm(request.POST)
        formset = CommentPictureFormset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.published_date = timezone.now()
            comment.save()

            for form_instance in formset:
                form_data = form_instance.save(commit=False)
                form_data.comment = comment
                form_data.save()
                save_activity(user, post, 'commented on', False)
                return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = CommentForm()
        formset = CommentPictureFormset()
    return render(request, "forum/post_details.html", {'form': form, 'formset':formset})

def comment_details(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    form = ReplyForm()
    context = {
        'comment': comment,
        'form': form
    }
    return render(request, 'forum/comment_details.html', context)

@login_required
def post_comment_edit(request, post_id, comment_id):
    get_post = get_object_or_404(Post, pk=post_id)
    get_comment = get_object_or_404(Comment, pk=comment_id)
    CommentPictureFormset = inlineformset_factory(Comment, CommentPicture, fields=('picture',))
    user = request.user
    if user != get_comment.author:
        raise PermissionDenied('Forbidden')
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=get_comment)
        formset = CommentPictureFormset(request.POST, request.FILES, instance=get_comment)
        if form.is_valid():
            data = form.save()
            data.post = get_post
            data.author = request.user
            data.published_date = timezone.now()
            data.save()

        for form_instance in formset:
            form_data = form_instance.save(commit=False)
            form_data.comment = data
            form_data.save()
            return redirect('comment_details', comment_id=get_comment.pk)
    else:
        form = CommentForm(instance=get_comment)
        formset = CommentPictureFormset(instance=get_comment)
    return render(request, 'forum/edit_comment.html', {'form':form, 'formset':formset})


# flagging comment
@login_required
def comment_flag_redirect(request, comment_id):
    get_comment = get_object_or_404(Comment, pk=comment_id)
    context = {
        'get_comment': get_comment
    }
    return render(request, 'forum/comment_flag.html', context)

# ajax call to flag the comment
@login_required
def comment_flag_ajax(request, comment_id):
    data = {}
    user = request.user
    get_comment = get_object_or_404(Comment, pk=comment_id)
    if user in get_comment.user_array_flag_comment.all():
        data['flag'] = False
    get_comment.user_array_flag_comment.add(user)
    data['flag'] = True
    return JsonResponse(data)

# created non-asynch function becus the json data refused to bring expected response
# and i dont have time for nonsense. Will come back to it tho. Lol
# process the thumping up of comment
@login_required
def comment_thump_up(request, comment_id, post_id):
    user = request.user
    get_comment = get_object_or_404(Comment, pk=comment_id)
    get_post = get_object_or_404(Post, pk=post_id)
        # check if user has already thumped the comment
    if user not in get_comment.comment_thumped_up.all():
        get_comment.comment_thumped_up.add(user)
        save_activity(user, get_post, 'thumped up', True)
        thumped_notification(get_post, get_post.author, user, 'thumped up', True)

            # remove user from the manaytomany of thumped_down
            # because a user cannot thump_up and thump_down a comment. Need to choice
        if user in get_comment.comment_thumped_down.all():
            get_comment.comment_thumped_down.remove(user)
    else:
        get_comment.comment_thumped_up.remove(user)
    return redirect(get_post.get_absolute_url())


@login_required
def comment_thump_up_for_comment_main(request, comment_id):
    user = request.user
    data = {}
    get_comment = get_object_or_404(Comment, pk=comment_id)
    # check if user has already thumped the comment
    if user not in get_comment.comment_thumped_up.all():
        get_comment.comment_thumped_up.add(user)
        save_activity(user, get_comment.post, 'thumped up', False)
        thumped_notification(get_comment.post, get_comment.post.author, user, 'thumped up', True)
        data['added'] = True
        # remove user from the manaytomany of thumped_up
        # because a user cannot thump_up and thump_down a comment. Need to choice one
        if user in get_comment.comment_thumped_down.all():
            get_comment.comment_thumped_down.remove(user)
            data['already_thumped_down'] = True
    else:
        get_comment.comment_thumped_up.remove(user)
        data['added'] = False
    return JsonResponse(data)
    
    

# for thump down comment
@login_required
def comment_thump_down(request, comment_id, post_id):
    user = request.user
    get_comment = get_object_or_404(Comment, pk=comment_id)
    get_post = get_object_or_404(Post, pk=post_id)
    # check if user has already thumped the comment
    if user not in get_comment.comment_thumped_down.all():
        get_comment.comment_thumped_down.add(user)
        # remove user from the manaytomany of thumped_up
        # because a user cannot thump_up and thump_down a comment. Need to choice one
        if user in get_comment.comment_thumped_up.all():
            get_comment.comment_thumped_up.remove(user)
    else:
        get_comment.comment_thumped_down.remove(user)
    return redirect(get_post.get_absolute_url())

@login_required
def comment_thump_down_for_comment_main(request, comment_id):
    user = request.user
    data = {}
    get_comment = get_object_or_404(Comment, pk=comment_id)
    # check if user has already thumped the comment
    if user not in get_comment.comment_thumped_down.all():
        get_comment.comment_thumped_down.add(user)
        data['added'] = True
        # remove user from the manaytomany of thumped_up
        # because a user cannot thump_up and thump_down a comment. Need to choice one
        if user in get_comment.comment_thumped_up.all():
            get_comment.comment_thumped_up.remove(user)
            data['already_thumped_up'] = True
    else:
        get_comment.comment_thumped_down.remove(user)
        data['added'] = False
    return JsonResponse(data)
    

@login_required
def comment_reply(request, comment_id):
    get_comment = get_object_or_404(Comment, pk=comment_id)
    user = request.user
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.author = user
            form_data.comment = get_comment
            form_data.save()
            save_activity(user, get_comment.post, 'replied to a comment', False)
            return redirect('comment_details', get_comment.pk)
    else:
        form = ReplyForm()
    return render(request, 'forum/comment_details.html', {'form':form})


@login_required
def comment_reply_edit(request, reply_id, comment_id):
    get_comment = get_object_or_404(Comment, pk=comment_id)
    get_reply = get_object_or_404(CommentReply, pk=reply_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=get_reply)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.author = request.user
            form_data.comment = get_comment
            form_data.save()
            return redirect('comment_details', get_comment.pk)
    else:
        form = ReplyForm(instance=get_reply)
    return render(request, 'forum/comment_reply_edit.html', {'form':form})


@login_required
def comment_reply_flag_redirect(request, reply_id):
    get_reply = get_object_or_404(CommentReply, pk=reply_id)

    context = {
        'get_reply': get_reply
    }
    return render(request, 'forum/comment_reply_flag.html', context)

@login_required
def comment_reply_flag_ajax(request, reply_id):
    get_reply = get_object_or_404(CommentReply, pk=reply_id)
    user = request.user
    data = {}
    if user in get_reply.user_array_flag_comment_reply.all():
        data['flag'] = False
    get_reply.user_array_flag_comment_reply.add(user)
    data['flag'] = True
    return JsonResponse(data)


@login_required
def reply_thump_up(request, reply_id):
    get_reply = get_object_or_404(CommentReply, pk=reply_id)
    user = request.user
    data = {}

    # the below logic is similar to above function
    if user not in get_reply.reply_thumped_up.all():
        get_reply.reply_thumped_up.add(user)
        data['added'] = True
        if user in get_reply.reply_thumped_down.all():
            get_reply.reply_thumped_down.remove(user)
            data['already_thumped_down'] = True
    else:
        get_reply.reply_thumped_up.remove(user)
        data['added'] = False
    return JsonResponse(data)


    
@login_required
def reply_thump_down(request, reply_id):
    get_reply = get_object_or_404(CommentReply, pk=reply_id)
    user = request.user
    data = {}

    # the below logic is similar to above function
    if user not in get_reply.reply_thumped_down.all():
        get_reply.reply_thumped_down.add(user)
        data['added'] = True
        if user in get_reply.reply_thumped_up.all():
            get_reply.reply_thumped_up.remove(user)
            data['already_thumped_up'] = True
    else:
        get_reply.reply_thumped_down.remove(user)
        data['added'] = False
    return JsonResponse(data)


# for rendering post details which also save the number of which the object pk is viewed
def post_details(request, pk, slug):
    ImageFormset = formset_factory(CommentPictureForm, extra=3)
    formset = ImageFormset()
    form = CommentForm()
    try:
        post_details = Post.objects.get(pk=pk)
        post_details.view_number = F('view_number') + 1
        post_details.save()
    except Post.DoesNotExist:
        raise Http404('The thread doest not exist')
    context = {
        'post_details': post_details,
        'formset': formset,
        'form': form
        }
    return render(request, "forum/post_details.html", context)


# for generic and abstraction catergories
def general_catetgory_view(request, category_string):
    # queryset top 5 of the most viewed post
    general_popular = Post.objects.filter(category=category_string).exclude(post_hidden=True).\
        annotate(number_of_click=Count('view_number')).order_by('-number_of_click')[:6]
    # show top 20 of the new post entry
    general_newest = Post.objects.filter(category=category_string).exclude(post_hidden=True).order_by('-published_date')[1:20]
    # queryset 7 to 15 of the most viewed post
    general_popular2 = Post.objects.filter(category=category_string).exclude(post_hidden=True).\
        annotate(clicks=Count('view_number')).order_by('clicks')[7:15]
     # top 21 to 200 of the newest post
    general_newest2 = Post.objects.filter(category=category_string).exclude(post_hidden=True).order_by('-published_date')[21:200]
      # chain the queryset
    general_list = list(chain(general_popular, general_newest, general_popular2, general_newest2))
    paginator = Paginator(general_list, 30)
    page = request.GET.get('page')
    return paginator.get_page(page)


def academic_post_view(request):
    academic_posts = general_catetgory_view(request, 'academic')
    return render(request, 'forum/academic_post.html', {'academic_posts': academic_posts})


# algorithm for showing opportunity post
def opportunity_post_view(request):
    opportunity_posts = general_catetgory_view(request, 'opportunity')
    return render(request, 'forum/opportunity_post.html', {'opportunity_posts': opportunity_posts})



# Algorithm for rendering of business hub related post
def business_hub_view(request):
    business_posts = general_catetgory_view(request, 'business_hub')
    return render(request, 'forum/business_post.html', {'business_posts': business_posts})


# Algorithm for rendering of admission related post
def admission_view(request):
    admission_posts = general_catetgory_view(request, 'admission')
    return render(request, 'forum/admission_post.html', {'admission_posts': admission_posts})


# Algorithm for rendering of events related post
def events_view(request):
    events_posts = general_catetgory_view(request, 'event')
    return render(request, 'forum/events_post.html', {'events_posts': events_posts})


# Algorithm for rendering of politics related post
def politics_view(request):
    politics_posts = general_catetgory_view(request, 'politics')
    return render(request, 'forum/politics_post.html', {'politics_posts': politics_posts})


# Algorithm for rendering of award related post
def award_view(request):
    award_posts = general_catetgory_view(request, 'award_competition')
    return render(request, 'forum/award_post.html', {'award_posts': award_posts})


# Algorithm for rendering of relationship related post
def relationship_view(request):
    relationship_posts = general_catetgory_view(request, 'relationship')
    return render(request, 'forum/relationship_post.html', {'relationship_posts': relationship_posts})


# Algorithm for rendering of social life related post
def social_life_view(request):
    social_life = general_catetgory_view(request, 'social_life')
    return render(request, 'forum/social_life.html', {'social_life': social_life})


# Algorithm for rendering of creative_writing related post
def creative_writing_view(request):
    creative_writing_posts = general_catetgory_view(request, 'creative_writing')
    return render(request, 'forum/creative_writing_post.html', {'creative_writing_posts': creative_writing_posts})


# Algorithm for rendering of general related post
def general_view(request):
    general_posts = general_catetgory_view(request, 'general')
    return render(request, 'forum/general_post.html', {'general_posts': general_posts})
    
def nysc(request):
    nysc = general_catetgory_view(request, 'nysc')
    return render(request, 'forum/nysc.html', {'nysc': nysc})