# Generated by Django 5.1.4 on 2024-12-26 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0002_remove_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
