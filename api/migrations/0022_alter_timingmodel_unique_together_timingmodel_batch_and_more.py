# Generated by Django 5.0.6 on 2024-07-26 14:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0021_remove_timetablemodel_unique_timing_date_period_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="timingmodel",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="timingmodel",
            name="batch",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.batchmodel",
            ),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name="timingmodel",
            constraint=models.UniqueConstraint(
                fields=("name", "batch"), name="unique_name_per_batch"
            ),
        ),
        migrations.AddConstraint(
            model_name="timingmodel",
            constraint=models.UniqueConstraint(
                fields=("start", "end", "batch"), name="unique_time_slot_per_batch"
            ),
        ),
    ]