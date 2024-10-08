# Generated by Django 5.0.6 on 2024-07-27 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0023_alter_timingmodel_name"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="timetablemodel",
            name="unique_timing_date_period",
        ),
        migrations.AddConstraint(
            model_name="timetablemodel",
            constraint=models.UniqueConstraint(
                fields=("timing", "section", "date", "subject"),
                name="unique_timing_date_period",
            ),
        ),
    ]
