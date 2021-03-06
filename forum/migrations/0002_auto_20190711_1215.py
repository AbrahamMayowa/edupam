# Generated by Django 2.1.3 on 2019-07-11 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='comment_image')),
            ],
        ),
        migrations.RemoveField(
            model_name='like',
            name='like_by',
        ),
        migrations.RemoveField(
            model_name='like',
            name='number_of_likes',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='picture',
        ),
        migrations.AddField(
            model_name='comment',
            name='thumped_down',
            field=models.ManyToManyField(related_name='comment_thumped_down', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='thumped_up',
            field=models.ManyToManyField(related_name='comment_thumped_up', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='thumped_down',
            field=models.ManyToManyField(related_name='thumped_down', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='thumped_up',
            field=models.ManyToManyField(related_name='thumped_up', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='picture',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('academic', 'Academic'), ('opportunity', 'Opportunity'), ('business_hub', 'Business Hub'), ('admission', 'Admission'), ('politics', 'Politics'), ('award', 'Awards'), ('relationship', 'Relationship'), ('social_life', 'Social Life'), ('creative_writing', 'Creative Writing'), ('general', 'General'), ('youth_service', 'Youth Service')], max_length=50),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.AddField(
            model_name='commentpicture',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_pictures', to='forum.Comment'),
        ),
    ]
