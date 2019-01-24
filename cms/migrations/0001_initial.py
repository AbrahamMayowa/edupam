# Generated by Django 2.1.3 on 2019-01-20 14:16

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Journalism',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField()),
                ('slug', models.SlugField(max_length=150)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('draft_date', models.DateTimeField(auto_now_add=True)),
                ('number_of_views', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
