# Generated by Django 3.0.7 on 2020-06-28 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('herbarium', '0011_auto_20200625_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designation',
            name='creator',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='herbarium_designation_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='designation',
            name='modifier',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='herbarium_designation_modified', to=settings.AUTH_USER_MODEL),
        ),
    ]
