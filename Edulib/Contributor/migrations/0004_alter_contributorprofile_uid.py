# Generated by Django 4.1.7 on 2023-04-09 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("Contributor", "0003_alter_contributorprofile_subjects_of_interest_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contributorprofile",
            name="uid",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
