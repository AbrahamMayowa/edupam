from django.forms import ModelForm
from django import forms
from django.forms import modelformset_factory
from .models import Award, Category, Contestant


class AwardForm(ModelForm):

    class Meta:
        model = Award
        fields = ['organisation', 'award_name', 'vote_end', 'multiple_vote']


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['award_category', ]
        labels = {
            'award_category': 'Name of the Category'
        }
        widgets = {
            'award_category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the name of a category'
                }
            )
        }
ContestantFormset = modelformset_factory(Contestant,
    fields=['contestant_name', ],
    extra=1,
    widgets={
        'contestant_name': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the Name of a Contestant here'
            }
        )
    }
)