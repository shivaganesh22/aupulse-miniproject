# Generated by Django 5.1 on 2024-08-20 05:33

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0026_test"),
    ]

    operations = [
        migrations.AlterField(
            model_name="test",
            name="img",
            field=cloudinary.models.CloudinaryField(
                max_length=255, verbose_name="image"
            ),
        ),
    ]
