from django.shortcuts import render

from django.urls import reverse_lazy

from django.views.generic import CreateView

from .forms import UserForm


class SignUp(CreateView):
    form_class = UserForm
    success_url = 'http://localhost:8000'
    template_name = 'user/signup.html'