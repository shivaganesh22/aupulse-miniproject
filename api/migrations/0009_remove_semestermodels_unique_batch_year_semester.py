# Generated by Django 5.0.6 on 2024-07-18 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_remove_semestermodels_unique_batch_year_semester_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="semestermodels",
            name="unique_batch_year_semester",
        ),
    ]
