# Generated by Django 2.1.3 on 2019-05-13 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_auto_20190513_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalism',
            name='slug',
            field=models.SlugField(max_length=150),
        ),
    ]