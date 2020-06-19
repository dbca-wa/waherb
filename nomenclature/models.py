from django.contrib.postgres.fields import JSONField
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from waherb.utils import AuditMixin, ActiveMixin, smart_truncate


class Reference(AuditMixin, ActiveMixin):
    """A reference from which taxonomic-relevant information is extracted and used to classify
    specimens into taxonomic groups.
    May or may not be associated with a Reference object in the NSL database.
    """
    title = models.CharField(
        max_length=1024, help_text='The full title of the publication in which this reference was published.')
    nsl_url = models.URLField(max_length=256, blank=True, null=True)
    metadata = JSONField(default=dict, blank=True)

    def __str__(self):
        return smart_truncate(self.title)


TAXONOMIC_RANK_CHOICES = (
    ('Class', 'Class'),
    ('Division', 'Division'),
    ('Family', 'Family'),
    ('Form', 'Form'),
    ('Genus', 'Genus'),
    ('Kingdom', 'Kingdom'),
    ('Order', 'Order'),
    ('Phylum', 'Phylum'),
    ('Species', 'Species'),
    ('Subclass', 'Subclass'),
    ('Subfamily', 'Subfamily'),
    ('Subspecies', 'Subspecies'),
    ('Subvariety', 'Subvariety'),
    ('Unknown', 'Unknown'),
    ('Variety', 'Variety'),
)


class Name(MPTTModel, AuditMixin, ActiveMixin):
    """This model represents a name for a taxonomic grouping that has been published in the
    scientific literature.
    May or may not be associated with a Name object in the NSL database.
    """
    name = models.CharField(
        max_length=512, unique=True, help_text='A name that has been validly published in a reference.')
    rank = models.CharField(
        max_length=64, db_index=True, choices=TAXONOMIC_RANK_CHOICES,
        help_text='The relative position of a taxon in the taxonomic hierarchy.')
    parent = TreeForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='children')
    basionym = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='basionym_of')
    references = models.ManyToManyField(
        Reference, blank=True, help_text='Published references containing an instance of this name.')
    nsl_url = models.URLField(max_length=256, blank=True, null=True)
    metadata = JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name
