# Generated by Django 5.1.4 on 2025-01-16 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0020_adminuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adminuser',
            old_name='indetifier',
            new_name='identifier',
        ),
    ]
