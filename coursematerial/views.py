from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView
from .forms import FileForm, FileReviewForm, FileUploadForm
from .models import FileUpload, FileReview
from django.urls import reverse
from django.forms import modelformset_factory, formset_factory
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import PermissionDenied
import os
from django.conf import settings
from django.http import JsonResponse
from django.db.models import F




# it process past question info's form
@login_required
def file_info(request):
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.uploader = request.user
            info.save()
            return redirect('file_upload_view', info.pk)
    else:
        form = FileForm()
    context = {'form':form}
    return render(request, 'coursematerial/file_info.html', context)


# def view for uploading file
@login_required
def file_upload_view(request, pk):
    file_info = get_object_or_404(FileUpload, pk=pk)
    context = { 
            'file_info': file_info,}
 
    return render(request, 'coursematerial/upload_file.html', context)

def file_upload_ajax(request, pk):
    data = {}
    related_info = get_object_or_404(FileUpload, pk=pk)
    if request.method == 'POST' and request.user == related_info.uploader:
        file_form = FileUploadForm(request.POST, request.FILES)
        if file_form.is_valid():
            file_data = file_form.save(commit=False)
            file_data.file_info = related_info
            file_data.save()
            data['successful'] = True
            data['message'] = 'You have successfully uploaded file(s)'
    else:
        data['successful'] = False
        data['message'] = 'File uplaod unsuccessful'
    return JsonResponse(data)


# Past question download page view
def file_detail(request, pk):
    review_form = FileReviewForm()
    try:
        file_data = FileUpload.objects.get(pk=pk)
    except FileUpload.DoesNotExist:
        raise Http404("There is no file for this course. Please upload a file when you see one!")
    review_list = file_data.course_file.order_by('-upload_time')
    context = {
        'file_data': file_data,
        'review_form': review_form,
        'review_list': review_list
    }
    return render(request, "coursematerial/course_details.html", context)



# this view process request for past question image download
def file_download(request, path, pk):
    """ this function fetch file url and automatically download it 
     and it also increase number of download field of the object"""
    get_file_object = get_object_or_404(FileUpload, pk=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        get_file_object.time_of_download = F('time_of_download') + 1
        get_file_object.save()
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'attachment; filename=' + 'edupam.com/' + os.path.basename(file_path)
            return response
    raise Http404('He file is non-exist or deleted')


# review of past question
@login_required
def file_review(request, pk):
    file_data = get_object_or_404(FileUpload, pk=pk)
    if request.method == 'POST':
        review_form = FileReviewForm(request.POST)
        if review_form.is_valid():
            review_save = review_form.save(commit=False)
            review_save.course_file = file_data
            review_save.review_author = request.user
            review_save.save()
            return redirect('file_detail', file_data.pk)
    else:
        review_form = FileReviewForm()
    return render(request, 'coursematerial/course_details.html', {'review_form':review_form})


@login_required
def edit_file_review(request, question_id, review_id):
    get_course = get_object_or_404(FileUpload, pk=question_id)
    get_review = get_object_or_404(FileReview, pk=review_id)
    if request.user == get_review.review_author and request.method == 'POST':
        form = FileReviewForm(request.POST, instance=get_review)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.course_file = get_course
            form_data.review_author = request.user
            form_data.save()
            return redirect('file_detail', get_course.pk)
    else:
        form = FileReviewForm(instance=get_review)
    return render(request, "coursematerial/file_review_edit.html", {'form': form})

    









# Create your views here.   
