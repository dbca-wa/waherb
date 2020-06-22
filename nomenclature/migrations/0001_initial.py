# Generated by Django 3.0.7 on 2020-06-19 05:16

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('effective_to', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(help_text='The full title of the publication in which this reference was published.', max_length=1024)),
                ('nsl_url', models.URLField(blank=True, max_length=256, null=True)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('creator', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='nomenclature_reference_created', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='nomenclature_reference_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('effective_to', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(help_text='A name that has been validly published in a reference.', max_length=512, unique=True)),
                ('rank', models.CharField(choices=[('Class', 'Class'), ('Division', 'Division'), ('Family', 'Family'), ('Form', 'Form'), ('Genus', 'Genus'), ('Kingdom', 'Kingdom'), ('Order', 'Order'), ('Phylum', 'Phylum'), ('Species', 'Species'), ('Subclass', 'Subclass'), ('Subfamily', 'Subfamily'), ('Subspecies', 'Subspecies'), ('Subvariety', 'Subvariety'), ('Unknown', 'Unknown'), ('Variety', 'Variety')], db_index=True, help_text='The relative position of a taxon in the taxonomic hierarchy.', max_length=64)),
                ('nsl_url', models.URLField(blank=True, max_length=256, null=True)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('basionym', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='basionym_of', to='nomenclature.Name')),
                ('creator', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='nomenclature_name_created', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='nomenclature_name_modified', to=settings.AUTH_USER_MODEL)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='nomenclature.Name')),
                ('references', models.ManyToManyField(blank=True, help_text='Published references containing an instance of this name.', to='nomenclature.Reference')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]