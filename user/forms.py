from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserInfo


# form for creating  custom users info
class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserInfo
        fields = ('username', 'first_name', 'last_name', 'email', 'school', 'location')


# Form for changing user info. This is subject to further alteration
class ChangeUser(ModelForm):
    class Meta:
        model = UserInfo
        fields = ('username', 'first_name', 'last_name', 'email', 'school', 'location',)

class ProfilePictureForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ['profile_picture']

class ProfileHeaderForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ['header_picture']
