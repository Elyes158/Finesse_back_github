# Generated by Django 5.1.4 on 2024-12-27 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0010_usergoogle'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergoogle',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='usergoogle',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='usergoogle',
            name='isPrivacyChecked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usergoogle',
            name='isSendMailChacked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usergoogle',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usergoogle',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
