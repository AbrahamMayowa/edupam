from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms import modelformset_factory
from django.db.models import F


from .models import Award, Category, Contestant
from .forms import AwardForm, CategoryForm, ContestantFormset
from user.models import UserInfo


@login_required(login_url='/user/login/')
def award_view(request):
    if request.method == "POST":
        award_form = AwardForm(request.POST)
        # validating both awardform
        if award_form.is_valid():
            # saving post to the db
            award = award_form.save(commit=False)
            award.starting = timezone.now()
            award.save()

            return redirect('get_award', pk=award.pk)
    else:
        award_form = AwardForm()

    context = {
        'award_form': award_form
    }

    return render(request, "voting/award_voting_home.html", context)

# award details 
def get_award(request, pk):
    award_detail = get_object_or_404(Award, pk=pk)

    context = {
        'award_detail': award_detail
    }

    return render(request, 'voting/get_award.html', context)


def category_and_contestant(request, pk):
    the_award = get_object_or_404(Award, pk=pk)
    template_name = 'voting/category_form.html'
    if request.method == 'GET':
        category_form = CategoryForm(request.GET or None)
        formset = ContestantFormset(queryset=Contestant.objects.none())
    elif request.method == 'POST':
        category_form = CategoryForm(request.POST)
        formset = ContestantFormset(request.POST)
        if category_form.is_valid() and formset.is_valid():
            # first save this book, as its reference will be used in `Author`
            save_category = category_form.save(commit=False)
            save_category.award = the_award
            save_category.save()

            for form in formset:
                # so that `book` instance can be attached.
                contest = form.save(commit=False)
                contest.award_name = the_award
                contest.category = save_category
                contest.save()

            return redirect('create_more', pk=the_award.pk)
    return render(request, template_name, {
        'category_form': category_form,
        'formset': formset,
})

def create_more(request, pk):
    the_award = Award.objects.get(pk=pk)
    the_award_category = the_award.awards_set.all()

    context = {
        'the_award': the_award
    }
    return render(request, 'voting/create_more_category.html', context)


# an award details view
def award_details(request, pk):
    get_award_details = get_object_or_404(Award, pk=pk)

    context = {
        'get_award_details': get_award_details
    }

    return render(request, 'voting/award_details', context)


# The view for voting
def category_details(request, pk):
    try:
        all_category = get_object_or_404(Category, pk=pk)
    except Category.DoesNotExist:
        raise Http404('The category is non-exist')
    context = {
        'all_category': all_category
    }

    return render(request, "voting/category_voting.html", context)


def award_list(request):
    all_award = Award.objects.all().order_by('-id')

    context = {
        'all_award': all_award
    }
    return render(request, 'voting/award_list.html', context)


def saving_vote(request, pk):
    voted_award = get_object_or_404(Award, pk=pk)
    the_voters = voted_award.category_set.get(pk=pk)

    try:
            selected_contestant = voted_award.contestant_set.get(pk=request.POST['contestant_name'])
            one_vote = voted_award.category_set.get(pk=pk)
    except (KeyError, Contestant.DoesNotExist):
        return render(request, "voting/category_voting.html",
                          {'voted_award': voted_award, 'error_message': "You didn't vote."})
    else:
        selected_contestant.vote = F('vote') + 1
        selected_contestant.save()
        one_vote.voters = request.user
        one_vote.save()
        return redirect('voting/result.html', voted_award.pk)

    return render(request, 'voting/category_voting.html', {'voted_award': voted_award, 'error_message': "You can't vote more than once."})


def result_view(request, pk):
    award_result = get_object_or_404(Award, pk=pk)

    context = {
        'award_result': award_result
    }

    return render(request, 'voting/result.html', context)
















# Create your views here.
