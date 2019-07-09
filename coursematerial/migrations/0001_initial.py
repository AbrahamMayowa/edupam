# Generated by Django 2.1.3 on 2019-07-05 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_file', models.FileField(blank=True, null=True, upload_to='course_file')),
            ],
        ),
        migrations.CreateModel(
            name='FileReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(max_length=1000)),
                ('upload_time', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=50)),
                ('course_title', models.CharField(max_length=100)),
                ('school_name', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('time_of_download', models.IntegerField(default=0)),
                ('upload_time', models.DateField(auto_now_add=True)),
                ('file_type', models.CharField(choices=[('past_question', 'Past Question'), ('course_material', 'Course Material')], max_length=50)),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='filereview',
            name='course_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_file', to='coursematerial.FileUpload'),
        ),
        migrations.AddField(
            model_name='filereview',
            name='review_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coursefile',
            name='file_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_info', to='coursematerial.FileUpload'),
        ),
    ]
