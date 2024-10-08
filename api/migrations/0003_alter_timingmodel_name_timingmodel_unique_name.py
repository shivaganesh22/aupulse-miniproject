# Generated by Django 5.0.6 on 2024-07-05 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_alter_semestermodels_batch"),
    ]

    operations = [
        migrations.AlterField(
            model_name="timingmodel",
            name="name",
            field=models.CharField(max_length=10),
        ),
        migrations.AddConstraint(
            model_name="timingmodel",
            constraint=models.UniqueConstraint(fields=("name",), name="unique_name"),
        ),
    ]
