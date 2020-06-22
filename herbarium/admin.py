from django.contrib import admin
from reversion.admin import VersionAdmin
from waherb.utils import ModelDescMixin, ActiveAdminMixin, WALeafletGeoAdmin
from .models import (
    Attachment, Annotation, Transaction, Agent, Address, Project, Permit, CollectingEvent,
    Determination, Specimen,
)


@admin.register(Attachment)
class AttachmentAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    list_display = ('upload', 'modified', 'modifier')
    list_filter = ('type',)
    readonly_fields = ('metadata',)
    search_fields = ('type', 'upload', 'description')


@admin.register(Annotation)
class AnnotationAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    list_display = ('type', 'annotation', 'modified', 'modifier')
    list_filter = ('type',)
    readonly_fields = ('metadata',)
    search_fields = ('type', 'annotation')


@admin.register(Transaction)
class TransactionAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    list_display = ('type', 'description', 'modified', 'modifier')
    list_filter = ('type',)
    readonly_fields = ('metadata',)
    search_fields = ('type', 'description')


@admin.register(Agent)
class AgentAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    list_display = ('name', 'type', 'email', 'member_of', 'modified', 'modifier')
    list_filter = ('type',)
    #raw_id_fields = ('attachments',)
    readonly_fields = ('metadata',)
    search_fields = ('name', 'type', 'email', 'member_of__name')


@admin.register(Address)
class AddressAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    list_display = ('agent', 'address_line_1', 'suburb', 'state', 'modified', 'modifier')
    readonly_fields = ('metadata',)
    search_fields = (
        'agent__name', 'address_line_1', 'address_line_2', 'suburb', 'city', 'state',
        'postcode', 'country')


@admin.register(Project)
class ProjectAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    list_display = ('name', 'modified', 'modifier')
    readonly_fields = ('metadata',)
    search_fields = ('name',)


@admin.register(Permit)
class PermitAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    list_display = ('permit_no', 'modified', 'modifier')
    readonly_fields = ('metadata',)
    search_fields = ('permit_no',)


@admin.register(CollectingEvent)
class CollectingEventAdmin(ModelDescMixin, ActiveAdminMixin, WALeafletGeoAdmin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    date_hierarchy = 'date'
    list_display = ('agent', 'project', 'permit', 'date', 'modified', 'modifier')
    readonly_fields = ('metadata',)
    search_fields = ('agent__name', 'project__name', 'permit__permit_no', 'description', 'location_description')


@admin.register(Specimen)
class SpecimenAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    list_display = ('barcode', 'event', 'collection', 'linear_sequence', 'modified', 'modifier')
    readonly_fields = ('metadata',)
    search_fields = ('barcode', 'collection', 'linear_sequence')


@admin.register(Determination)
class DeterminationAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    date_hierarchy = 'date'
    list_display = ('agent', 'name', 'specimen', 'date', 'modified', 'modifier')
    readonly_fields = ('metadata',)
    search_fields = ('agent__name', 'name__name', 'specimen__barcode')
