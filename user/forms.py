from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserInfo


# form for creating  custom users info
class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserInfo
        fields = ('username', 'email', 'school', 'faculty',)


# Form for changing user info. This is subject to further alteration
class ChangeUser(UserChangeForm):
    class Meta:
        model = UserInfo
        fields = ('username', 'email', 'school', 'faculty',)
