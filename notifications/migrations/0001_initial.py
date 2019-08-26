# Generated by Django 2.1.3 on 2019-07-21 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_action_verb', models.CharField(max_length=150)),
                ('target_id', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('view_status', models.BooleanField(default=False)),
                ('comment_performer_list', models.ManyToManyField(related_name='commentors', to=settings.AUTH_USER_MODEL)),
                ('model_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_author_notification', to=settings.AUTH_USER_MODEL)),
                ('target_comment_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_notification', to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='GeneralNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('action_verb_general', models.CharField(max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('view_status', models.BooleanField(default=False)),
                ('content_type_general', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='general_target_model', to='contenttypes.ContentType')),
                ('content_type_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='general_notification_author', to=settings.AUTH_USER_MODEL)),
                ('performer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='general_user_perfomers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalisedCommentNotif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal_action_verb', models.CharField(max_length=50)),
                ('view_status', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('notification_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personal_comment_notification', to=settings.AUTH_USER_MODEL)),
                ('related_comment_notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented_user', to='notifications.CommentNotification')),
            ],
        ),
        migrations.CreateModel(
            name='ThumpedNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_id', models.PositiveIntegerField()),
                ('thumped_action_string', models.CharField(max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('view_status', models.BooleanField(default=False)),
                ('actor_list', models.ManyToManyField(related_name='thumped_list', to=settings.AUTH_USER_MODEL)),
                ('thumped_content_type_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models_author', to=settings.AUTH_USER_MODEL)),
                ('thumped_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thumped_up_target', to='contenttypes.ContentType')),
            ],
        ),
    ]