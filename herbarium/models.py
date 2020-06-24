from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
import json
from waherb.utils import AuditMixin, ActiveMixin, smart_truncate
from nomenclature.models import Name


class TexpressData(models.Model):
    """Data from the legacy Texpress database, loaded for the purposes of migration & archive.
    """
    row = JSONField(default=dict, blank=True)
    row_text = models.TextField(help_text='Document for search', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'texpress data'
        indexes = [GinIndex(fields=['row'])]

    def __str__(self):
        # Don't just use the string repr of the JSONField, as that outputs single quotes
        # which is confusing to end users as it differs from what's stored in the DB.
        s = '{}'.format(json.dumps(self.row, sort_keys=True, separators=(',', ':')))
        return smart_truncate(s, length=200)


ATTACHMENT_TYPE_CHOICES = (
    ('Specimen photo', 'Specimen photo'),
)


class Attachment(AuditMixin, ActiveMixin):
    """An uploaded electronic file that can be attached to other objects in the system.
    """
    type = models.CharField(max_length=64, choices=ATTACHMENT_TYPE_CHOICES, blank=True, null=True)
    upload = models.FileField(max_length=1024, upload_to='uploads/%Y/%m/%d')
    description = models.TextField(blank=True, null=True)
    metadata = JSONField(default=dict, blank=True)

    def __str__(self):
        return self.upload.file.name


ANNOTATION_TYPE_CHOICES = (
    ('File note', 'File note'),
)


class Annotation(AuditMixin, ActiveMixin):
    """This model represents some piece of information placed on another object.
    It might be something like a file note, etc.
    """
    type = models.CharField(max_length=64, choices=ANNOTATION_TYPE_CHOICES)
    annotation = models.TextField()
    attachment = models.ForeignKey(Attachment, on_delete=models.SET_NULL, blank=True, null=True)
    metadata = JSONField(default=dict, blank=True)


TRANSACTION_TYPE_CHOICES = (
    ('Accession', 'Accession'),
    ('Loan out', 'Loan out'),
    ('Loan return', 'Loan return'),
)


class Transaction(AuditMixin, ActiveMixin):
    """A transaction represents some interaction with the system by an agent that
    needs to be recorded in detail.
    """
    type = models.CharField(max_length=64, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField()
    attachment = models.ForeignKey(Attachment, on_delete=models.SET_NULL, blank=True, null=True)
    metadata = JSONField(default=dict, blank=True)


AGENT_TYPE_CHOICES = (
    ('Person', 'Person'),
    ('Organisation', 'Organisation'),
    ('Other', 'Other'),
)


class Agent(AuditMixin, ActiveMixin):
    """A general-purpose model type for a person or organisation out in the world that needs
    to be associated with other records in this system.
    """
    name = models.CharField(max_length=256, unique=True, help_text='A unique name for this agent.')
    type = models.CharField(
        max_length=64, choices=AGENT_TYPE_CHOICES, help_text='An "agent" can be a person or a group.')
    email = models.EmailField(blank=True, null=True, help_text='A valid email address.')
    member_of = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='members',
        help_text='An agent can be a member of a different agent (e.g. a person can be a member of a group).')
    attachments = models.ManyToManyField(Attachment, blank=True)
    metadata = JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name


class Address(AuditMixin, ActiveMixin):
    """A physical or mailing address within Australia, associated with an Agent.
    """
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='addresses')
    address_line_1 = models.CharField(max_length=256, blank=True, null=True)
    address_line_2 = models.CharField(max_length=256, blank=True, null=True)
    suburb = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    state = models.CharField(max_length=256, blank=True, null=True)
    postcode = models.CharField(max_length=16, blank=True, null=True)
    country = models.CharField(max_length=256, blank=True, null=True, default='Australia')
    telephone = models.CharField(max_length=32, blank=True, null=True)
    fax = models.CharField(max_length=32, blank=True, null=True)
    is_primary = models.BooleanField(null=True)
    metadata = JSONField(default=dict, blank=True)

    class Meta:
        verbose_name_plural = 'addresses'


class Project(AuditMixin, ActiveMixin):
    name = models.CharField(max_length=256, unique=True, help_text='A unique name for this project.')
    metadata = JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name


class Permit(AuditMixin, ActiveMixin):
    permit_no = models.CharField(
        max_length=256, unique=True, help_text='A unique permit number (normally generated by an external system).')
    metadata = JSONField(default=dict, blank=True)

    def __str__(self):
        return self.permit_no


TEMPORAL_ACCURACY_CHOICES = (
    ('Year', 'Year'),
    ('Month', 'Month'),
    ('Day', 'Day'),
)
SPATIAL_ACCURACY_CHOICES = (
    ('10000 m', '10000 m'),
    ('1000 m', '1000 m'),
    ('100 m', '100 m'),
    ('10 m', '10 m'),
    ('1 m', '1 m'),
)


class CollectingEvent(AuditMixin, ActiveMixin):
    """This represents a singular event where an Agent went out and collected one or more
    Specimens in the world.
    """
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, related_name='collecting_events')
    project = models.ForeignKey(Project, on_delete=models.PROTECT, blank=True, null=True, related_name='collecting_events')
    permit = models.ForeignKey(Permit, on_delete=models.PROTECT, blank=True, null=True, related_name='collecting_events')
    date = models.DateField(blank=True, null=True)
    temporal_accuracy = models.CharField(max_length=64, choices=TEMPORAL_ACCURACY_CHOICES, blank=True, null=True)
    description = models.TextField(blank=True, null=True, help_text='A description of the collection event.')
    location_description = models.TextField(
        blank=True, null=True, help_text='A description of where the collection event was undertaken.')
    point = models.PointField(srid=4283, blank=True, null=True)
    spatial_accuracy = models.CharField(max_length=64, choices=SPATIAL_ACCURACY_CHOICES, blank=True, null=True)
    annotations = models.ManyToManyField(Annotation, blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)
    metadata = JSONField(default=dict, blank=True)


class Specimen(AuditMixin, ActiveMixin):
    """This model represents a physical specimen that is held by the Herbarium.
    """
    barcode = models.CharField(max_length=256, unique=True, help_text='Unique barcode (sheet no.)')
    event = models.ForeignKey(CollectingEvent, on_delete=models.PROTECT, blank=True, null=True, related_name='specimens')
    collection = models.CharField(max_length=256, blank=True, null=True)
    linear_sequence = models.CharField(max_length=32, blank=True, null=True)
    annotations = models.ManyToManyField(Annotation, blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)
    metadata = JSONField(default=dict, blank=True)


class Determination(AuditMixin, ActiveMixin):
    """This represents an event where an Agent classified a Specimen as a particular taxon.
    """
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, related_name='determiner')
    name = models.ForeignKey(Name, on_delete=models.PROTECT)
    specimen = models.ForeignKey(Specimen, on_delete=models.PROTECT)
    date = models.DateField()
    annotations = models.ManyToManyField(Annotation, blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)
    metadata = JSONField(default=dict, blank=True)
