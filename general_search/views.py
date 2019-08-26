from django.shortcuts import render
from .forms import SearchForm
from itertools import chain
from operator import attrgetter
from voting.models import Award, Contestant
from forum.models import Post
from coursematerial.models import FileUpload
from cms.models import Journalism


def general_search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search']
            if search_query:
                get_coursematerial = FileUpload.objects.search(search_query)
                get_post = Post.objects.search(search_query)
                get_award = Award.objects.search(search_query)
                get_contestant = Contestant.objects.search(search_query)
                get_journalism = Journalism.objects.search(search_query)
                chained_queryset = chain(get_coursematerial, get_post, get_award, get_contestant, get_journalism)
                queryset = sorted(chained_queryset, key=attrgetter('created'), reverse=True)
    context = {
        'queryset': queryset,
    }
    return render(request, 'general_search/search.html', context)
                

            






