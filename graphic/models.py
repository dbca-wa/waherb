from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.db import models


class Node(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    metadata = JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('content_type', 'object_id')

    def __str__(self):
        return '{} {}'.format(self.content_type.model_class()._meta.verbose_name.capitalize(), self.content_object)


class Edge(models.Model):
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='source')
    target = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='target')
    type = models.CharField(max_length=64, db_index=True)  # TODO: rename to "label".
    metadata = JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('source', 'target', 'type')

    def __str__(self):
        return '{} {} {}'.format(self.source.content_object, self.type, self.target.content_object)
