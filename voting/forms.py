from django.forms import ModelForm
from .models import Award, Category, Contestant


class AwardForm(ModelForm):

    class Meta:
        model = Award
        fields = ['organisation', 'award_name', 'vote_end', 'voting_nature']


class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['award_category', ]


class ContestantForm(ModelForm):

    class Meta:
        model = Contestant
        fields = ['award_name', 'contestant_name', 'category']