# Generated by Django 3.0.7 on 2020-06-22 06:57

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herbarium', '0002_texpressdata'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='texpressdata',
            options={'verbose_name_plural': 'texpress data'},
        ),
        migrations.AddIndex(
            model_name='texpressdata',
            index=django.contrib.postgres.indexes.GinIndex(fields=['row'], name='herbarium_t_row_2796a7_gin'),
        ),
    ]
