from django.db import models


class PastQuestion(models.Model):
    image = models.ImageField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    course_code = models.CharField(blank=False, max_length=30, default='POS 211')
    course_title = models.CharField(blank=False, max_length=100, default='Introduction to Sociology')
    school = models.CharField(max_length=50, null=True)
    download = models.IntegerField()
    number_of_share = models.IntegerField()
    review = models.TextField(max_length=100, default='This past question save my life!')
    post_by = models.CharField(max_length=50, blank=True, null=True)


class CourseMaterial(models.Model):
    file = models.FileField(blank=False, null=False)
    course_title = models.CharField(max_length=100, blank=False, default='Politics in Africa')
    course_code = models.CharField(max_length=30, blank=False, default='POS 111')
    material_title = models.CharField(max_length=100, null=True, blank=True)
    shared_by = models.CharField(max_length=30, null=True)
    review = models.TextField(max_length=100, null=True)


class Shares(models.Model):

    number_of_course_material_shares = models.OneToOneField(CourseMaterial, on_delete=models.CASCADE,
                                                            default=5)
    number_of_past_question_share = models.OneToOneField(PastQuestion, primary_key=True, on_delete=models.CASCADE,
                                                         default=5)


class Download(models.Model):
    number_of_download_course_material = models.ForeignKey(CourseMaterial,
                                                           on_delete=models.CASCADE,
                                                           related_name='downloads', default=5)
    number_of_download_past_question = models.ForeignKey(PastQuestion,
                                                         on_delete=models.CASCADE,
                                                         related_name='question_number', default=5)








# Create your models here.
