# Generated by Django 2.1.3 on 2019-05-04 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20190504_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalism',
            name='slug',
            field=models.SlugField(max_length=150),
        ),
    ]