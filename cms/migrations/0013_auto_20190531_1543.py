# Generated by Django 2.1.3 on 2019-05-31 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20190529_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalism',
            name='claps',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]