from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from reversion.admin import VersionAdmin
from waherb.utils import ModelDescMixin, ActiveAdminMixin
from .models import Reference, Name


class NSLURLFilter(admin.SimpleListFilter):
    """SimpleListFilter to filter on True/False if an object has a value for nsl_url.
    """
    title = 'NSL URL'
    parameter_name = 'nsl_url_boolean'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Present'),
            ('false', 'Absent'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(nsl_url__isnull=False)
        if self.value() == 'false':
            return queryset.filter(nsl_url__isnull=True)


@admin.register(Reference)
class ReferenceAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    fields = ('title', 'nsl_url', 'metadata')
    list_display = ('title_trunc', 'nsl_url_link', 'modified', 'modifier')
    list_filter = (NSLURLFilter,)
    model_description = """A reference from which taxonomic-relevant information is extracted and
        used to classify specimens into taxonomic groups."""
    search_fields = ('title',)

    def title_trunc(self, obj):
        return str(obj)
    title_trunc.short_description = 'title'

    def nsl_url_link(self, obj):
        if obj.nsl_url:
            return mark_safe('<a href="{0}" target="_blank">{0}</a>'.format(obj.nsl_url))
        return ''
    nsl_url_link.short_description = 'NSL URL'


@admin.register(Name)
class NameAdmin(ModelDescMixin, VersionAdmin):

    class HasParentFilter(admin.SimpleListFilter):
        """SimpleListFilter to filter on True/False if an object has a value for parent.
        """
        title = 'has parent'
        parameter_name = 'parent_boolean'

        def lookups(self, request, model_admin):
            return (
                ('true', 'True'),
                ('false', 'False'),
            )

        def queryset(self, request, queryset):
            if self.value() == 'true':
                return queryset.filter(parent__isnull=False)
            if self.value() == 'false':
                return queryset.filter(parent__isnull=True)

    fields = ('name', 'rank', 'parent', 'basionym', 'references', 'nsl_url', 'metadata')
    filter_horizontal = ('references',)
    list_display = ('name', 'rank', 'parent', 'nsl_url_link', 'taxon_tree', 'modified', 'modifier')
    list_filter = ('rank', NSLURLFilter, HasParentFilter)
    model_description = 'A scientific name that has been classified into a taxonomic tree.'
    raw_id_fields = ('references', 'parent', 'basionym')
    search_fields = ('name', 'rank', 'parent__name', 'basionym__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Return 'current' (non-deleted) objects only.
        return qs.filter(effective_to=None)

    def nsl_url_link(self, obj):
        if obj.nsl_url:
            return mark_safe('<a href="{0}" target="_blank">{0}</a>'.format(obj.nsl_url))
        return ''
    nsl_url_link.short_description = 'NSL URL'

    def taxon_tree(self, obj):
        return mark_safe('<a href="{}" target="_blank">Link</a>'.format(reverse('nomenclature:taxon_tree', kwargs={'pk': obj.pk})))
