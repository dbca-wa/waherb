from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse


class CrossReference(models.Model):
    """A general-purpose model which can relate any object (`content_object`) to any other
    object (`target_content_object`), which associated metadata about the relationship.
    The intent is to provide functionality similar to that found in a graph database using the
    stock Django ORM. It is similar to an XREF table, but does not restrict the linked tables
    like a normal M2M relationship.
    """
    metadata = JSONField(default=dict, blank=True)
    ref_type = models.CharField(
        max_length=64, db_index=True, default='relates to',
        help_text='A short textual description for how the object relates to the target object')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='content_type')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='target_content_type')
    target_object_id = models.PositiveIntegerField()
    target_content_object = GenericForeignKey('target_content_type', 'target_object_id')

    def __str__(self):
        return '{} {} {}'.format(str(self.content_object), self.ref_type, str(self.target_content_object))

    def get_absolute_url(self):
        return reverse('cross_reference_detail', kwargs={'pk': self.pk})

    def get_obj_model_name(self):
        return self.content_object._meta.model._meta.verbose_name

    def get_target_model_name(self):
        return self.target_content_object._meta.model._meta.verbose_name
