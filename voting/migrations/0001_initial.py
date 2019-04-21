# Generated by Django 2.1.3 on 2019-04-17 23:45

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
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation', models.CharField(blank=True, max_length=200, null=True)),
                ('award_name', models.CharField(max_length=200)),
                ('starting', models.DateField(auto_now_add=True)),
                ('vote_end', models.DateField()),
                ('multiple_vote', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('award_category', models.CharField(blank=True, max_length=150, null=True)),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awards', to='voting.Award')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contestant_name', models.CharField(blank=True, max_length=150, null=True)),
                ('vote', models.IntegerField()),
                ('award_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contestant_awards', to='voting.Award')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='voting.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Voters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('the_voters', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voting.Category')),
            ],
        ),
    ]
