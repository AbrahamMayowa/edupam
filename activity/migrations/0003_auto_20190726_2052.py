# Generated by Django 2.1.3 on 2019-07-26 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_auto_20190726_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='activities',
            name='object_id',
            field=models.PositiveIntegerField(),
        ),
    ]
