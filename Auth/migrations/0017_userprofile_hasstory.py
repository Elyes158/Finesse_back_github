# Generated by Django 5.1.4 on 2025-01-01 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0016_remove_userprofile_story_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='hasStory',
            field=models.BooleanField(default=False),
        ),
    ]
