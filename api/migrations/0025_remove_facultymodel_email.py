# Generated by Django 5.0 on 2024-08-25 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_remove_timetablemodel_unique_timing_date_period_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facultymodel',
            name='email',
        ),
    ]
