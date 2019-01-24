from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.forms import modelformset_factory
from django.db.models import F


from .models import Award, Category, Contestant
from .forms import AwardForm, CategoryForm, ContestantForm
from user.models import UserInfo


@login_required(login_url='/user/login/')
def award_view(request):
    CategoryFormSet = modelformset_factory(Category, fields=('award_category',), extra=15)
    if request.method == "POST":
        award_form = AwardForm(request.POST)
        formset = CategoryFormSet(request.POST)
        # validating both awardform and categoryform
        if award_form.is_valid() and formset.is_valid():
            # saving post to the db
            award = award_form.save(commit=False)
            award.starting = timezone.now()
            award.save()
            # saving formset
            for category_entry in formset:
                try:
                    save_category = Category(award=award, award_category=category_entry.cleaned_data['award_category'],
                                             user=request.user)
                    save_category.save()
                except KeyError:
                    break
            return redirect('get_award', pk=award.pk)
    else:
        award_form = AwardForm()
        formset = CategoryFormSet(queryset=Category.objects.none())

    context = {
        'award_form': award_form,
        'formset': formset
    }

    return render(request, "voting/award_voting_home.html", context)


# the view that render form for creating contestants of an award
def get_award(request, pk):
    new_award = get_object_or_404(Award, pk=pk)
    Contest_Formset = modelformset_factory(Contestant, fields=('contestant_name', 'category',), extra=15)
    formset = Contest_Formset(request.POST)
    for form in formset:
        form.fields['category'].queryset = Category.objects.filter(user=request.user)[1:15]
        if request.method == 'POST' and form.is_valid():
            myform = form.save(commit=False)
            myform.award_name = new_award
            myform.save()
            return redirect('award_details', pk=new_award.pk)
    else:
        formset = Contest_Formset()

    context = {
        'new_award': new_award,
        'formset': formset
    }

    return render(request, 'voting/get_award.html', context)




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

    if voted_award.voting_nature == "True" and request.user not in the_voters.voters | voted_award.voting_nature == 'False':

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
    else:
        return render(request, 'voting/category_voting.html',
                      {'voted_award': voted_award, 'error_message': "You can't vote more than once."})


def result_view(request, pk):
    award_result = get_object_or_404(Award, pk=pk)

    context = {
        'award_result': award_result
    }

    return render(request, 'voting/result.html', context)
















# Create your views here.
