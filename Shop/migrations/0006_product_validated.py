# Generated by Django 5.1.4 on 2025-01-16 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0005_alter_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='validated',
            field=models.BooleanField(default=False),
        ),
    ]
