# Generated by Django 2.1.3 on 2019-08-19 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20190813_1200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='published_date',
            new_name='created',
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('academic', 'Academic'), ('opportunity', 'Opportunity'), ('business_hub', 'Business Hub'), ('admission', 'Admission'), ('politics', 'Politics'), ('award_competition', 'Awards and Competition'), ('relationship', 'Relationship'), ('social_life', 'Campus Social Life'), ('creative_writing', 'Creative Writing'), ('general', 'General'), ('nysc', 'NYSC')], max_length=50),
        ),
    ]
