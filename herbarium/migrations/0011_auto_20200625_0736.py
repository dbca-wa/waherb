# Generated by Django 3.0.7 on 2020-06-24 23:36

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nomenclature', '0001_initial'),
        ('herbarium', '0010_auto_20200624_1334'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Determination',
            new_name='Designation',
        ),
    ]
