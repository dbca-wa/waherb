from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from nomenclature.models import Name
from waherb.utils import AuditMixin, ActiveMixin


class Source(AuditMixin, ActiveMixin):
    """The model represents a source of data used to record the location(s) of identified taxa.
    """
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    custodian = models.CharField(
        max_length=256, blank=True, null=True, help_text='Name of the custodian of this data source.')


SUPRA_CODE_MAP = {
    'AMPHI': 'Amphibian',
    'FUNGUS': 'Fungus',
    'PROTIST': 'Protist',
    'BACTERIUM': 'Bacterium',
    'FISH': 'Fish',
    'MAMMAL': 'Mammal',
    'MONOCOT': 'Monocotyledeon',
    'DICOT': 'Dicotyledon',
    'FERN': 'Fern',
    'GYMNO': 'Gymnosperm',
    'INVERT': 'Invertebrate',
    'LICHEN': 'Lichen',
    'REPTILE': 'Reptile',
    'ALGA': 'Alga',
    'BIRD': 'Bird',
    'SLIMEMOULD': 'Slimemould',
    'MOSS': 'Moss',
    'LIVERWORT': 'Liverwort',
}


class TaxonLocation(AuditMixin, ActiveMixin):
    """This model represents a location in the world where a sample was collected, and later identified
    as a particular taxon.
    """
    name = models.CharField(max_length=512, help_text='The published scientific name of this taxon.')
    point = models.PointField(srid=4283)
    published_name = models.ForeignKey(Name, on_delete=models.PROTECT, blank=True, null=True)
    supra = models.CharField(
        max_length=64, blank=True, null=True, help_text='The supra group of this taxon.')
    family = models.CharField(
        max_length=64, blank=True, null=True, help_text='The taxonomic family of this taxon.')
    kingdom = models.CharField(
        max_length=64, blank=True, null=True, help_text='The taxonomic kingdom of this taxon.')
    conservation_status = models.CharField(
        max_length=16, blank=True, null=True, help_text='The conservation status of this taxon.')
    vernacular = models.CharField(
        max_length=256, blank=True, null=True, help_text='The common name of this taxon.')
    collector = models.CharField(
        max_length=256, help_text='The person(s) who collected/identified this taxon sample.')
    collected_date = models.DateField(
        blank=True, null=True, help_text='Date that this taxon sample was collected.')
    survey = models.CharField(
        max_length=256, help_text='The name of the survey during which this taxon sample was collected.')
    source = models.ForeignKey(Source, on_delete=models.PROTECT, blank=True, null=True)
    metadata = JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name
