from django.contrib import admin
from django.utils.safestring import mark_safe
import json
from reversion.admin import VersionAdmin
from waherb.utils import ModelDescMixin, ActiveAdminMixin, WALeafletGeoAdmin
from .models import (
    Attachment, Annotation, Transaction, Organisation, Person, Address, Project, Permit,
    Location, CollectingEvent, Designation, Specimen, TexpressData,
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


@admin.register(Address)
class AddressAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    list_display = ('address_line_1', 'suburb', 'state', 'modified', 'modifier')
    readonly_fields = ('metadata',)
    search_fields = (
        'address_line_1', 'address_line_2', 'suburb', 'city', 'state',
        'postcode', 'country')


@admin.register(Organisation)
class OrganisationAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    list_display = ('name', 'email', 'modified', 'modifier')
    readonly_fields = ('metadata',)
    search_fields = ('name', 'email', 'notes')


@admin.register(Person)
class PersonAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    list_display = ('name', 'type', 'email', 'modified', 'modifier')
    list_filter = ('type',)
    #raw_id_fields = ('attachments',)
    readonly_fields = ('metadata',)
    search_fields = ('name', 'type', 'email', 'notes')


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


@admin.register(Location)
class LocationAdmin(ModelDescMixin, ActiveAdminMixin, WALeafletGeoAdmin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    list_display = ('description', 'spatial_accuracy', 'modifier')
    list_filter = ('spatial_accuracy',)
    readonly_fields = ('metadata',)
    search_fields = ('description',)
    model_description = """This represents a physical location in the world. It might be a point
    or a polygon, and it might not be 100% accurate."""
    change_list_template = 'admin/herbarium/change_list.html'


@admin.register(CollectingEvent)
class CollectingEventAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    date_hierarchy = 'date'
    list_display = ('person', 'project', 'permit', 'date', 'modified', 'modifier')
    list_filter = ('temporal_accuracy',)
    readonly_fields = ('metadata',)
    search_fields = ('person__name', 'project__name', 'permit__permit_no', 'description', 'location_description')


@admin.register(Specimen)
class SpecimenAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    list_display = ('barcode', 'event', 'collection', 'linear_sequence', 'modified', 'modifier')
    readonly_fields = ('metadata',)
    search_fields = ('barcode', 'collection', 'linear_sequence')


@admin.register(Designation)
class DesignationAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    exclude = ('created', 'creator', 'modified', 'modifier', 'effective_to')
    date_hierarchy = 'date'
    list_display = ('person', 'name', 'specimen', 'date', 'modified', 'modifier')
    raw_id_fields = ('person', 'name', 'specimen')
    readonly_fields = ('metadata',)
    search_fields = ('person__name', 'name__name', 'specimen__barcode')


@admin.register(TexpressData)
class TexpressDataAdmin(admin.ModelAdmin):
    fields = ('row_pre',)
    readonly_fields = ('row_pre',)
    search_fields = ('row_text',)
    show_full_result_count = False
    save_on_top = True

    def row_pre(self, obj):
        return mark_safe('<pre>{}</pre>'.format(json.dumps(obj.row, indent=2, sort_keys=True, separators=(',', ':'))))
    row_pre.short_description = 'row data'

    def has_delete_permission(self, request, obj=None):
        # No one gets to delete these records (they're RO archives).
        return False

    def get_search_results(self, request, queryset, search_term):
        print(search_term)
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        # The default query that the ORM generates for this is pretty slow.
        # For performance, run a raw query over the indexed row_text column using the search term.
        # Then, use the list of PKs from that the filter the queryset.
        if search_term:
            search_term = search_term.replace('": "', '":"')  # Just in case someone still adds a space between key & value.
            raw_qs = TexpressData.objects.raw("SELECT * FROM herbarium_texpressdata WHERE row_text ILIKE '%%{}%%'".format(search_term))
            pks = [i.pk for i in raw_qs]
            queryset = queryset.filter(pk__in=pks)
        return queryset, use_distinct
