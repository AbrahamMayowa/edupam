# Generated by Django 2.1.3 on 2019-05-31 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_auto_20190531_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalism',
            name='claps',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='journalism',
            name='number_of_views',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]