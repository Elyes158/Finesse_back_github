# Generated by Django 5.1.4 on 2025-01-16 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0021_rename_indetifier_adminuser_identifier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adminuser',
            old_name='identifier',
            new_name='indetifier',
        ),
    ]
