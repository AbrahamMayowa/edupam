# Generated by Django 2.1.3 on 2019-06-01 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0015_auto_20190531_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalism',
            name='ranking_determination',
            field=models.IntegerField(default=0),
        ),
    ]