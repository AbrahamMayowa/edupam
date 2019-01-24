from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView
from .forms import FormForQuestion, FormForMaterial, FormForReviewing
from .models import PastQuestion, CourseMaterial
from django.urls import reverse


# def view for uploading past question
class FormForPastQuestion(FormView):
    form_class = FormForQuestion
    template_name = 'upload_past_question.html'
    success_url = '#'

    def past_question_form(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image = request.FILES.get_list('image')
        if form.is_valid():
            for f in image:
                f.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# View for uploading course material.
def form_for_material_view(request):
    if request.method == 'POST':
        form = FormForMaterial(request.POST, request.FILE)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('UploadMaterial/')
    else:
        form = FormForMaterial()
    return render(request, "coursematerial/material_form.html", {'form': form})


# Past question download page view
def past_question_view(request, pk):
    try:
        past_question_file = PastQuestion.objects.get(pk=pk)
    except PastQuestion.DoesNotExist:
        raise Http404("There is no past question for this course. Please upload the question file when you see one!")
    context = {
        'past_question_file': past_question_file
    }
    return render(request, "coursematerial/download_past_question.html", context)


# review of past question
def question_review_form(request):
    if request.method == 'POST':
        form_of_review = FormForReviewing(request.POST)
        if form_of_review.is_valid():
            form_of_review.save()
            return HttpResponseRedirect('download_question', pk=PastQuestion.pk)
    else:
        form_of_review = ()
    return render(request, "coursematerial/download_past_question.html", {'form_of_review': form_of_review})


# Edit the review
def edit_review_question(request, pk):
    form = get_object_or_404(PastQuestion, pk=pk)
    if request.method == 'POST':
        form = FormForReviewing(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('download_question', pk=PastQuestion.pk)
    else:
        form = FormForReviewing(instance=form)
    return render(request, "coursematerial/question_review_edit", {'form': form})


# Course Material download
def download_material(request, pk):
    try:
        material_list = CourseMaterial.objects.get(pk=pk)
    except CourseMaterial.DoesNotExist:
        raise Http404('The material is not available. Kindly upload one if you later have it')
    context = {
        'material_list': material_list
    }
    return render(request, "coursematerial/download_material.html", context)







# Create your views here.
