from django.contrib import admin
from reversion.admin import VersionAdmin
from waherb.utils import ModelDescMixin, ActiveAdminMixin
from .models import Reference, Name


@admin.register(Reference)
class ReferenceAdmin(ModelDescMixin, ActiveAdminMixin, VersionAdmin):
    fields = ('title', 'nsl_url', 'metadata')
    list_display = ('title_trunc', 'nsl_url', 'modified', 'modifier')
    model_description = """A reference from which taxonomic-relevant information is extracted and
        used to classify specimens into taxonomic groups."""
    search_fields = ('title',)
    change_list_template = 'admin/nomenclature/change_list.html'

    def title_trunc(self, obj):
        return str(obj)
    title_trunc.short_description = 'title'


@admin.register(Name)
class NameAdmin(ModelDescMixin, VersionAdmin):
    fields = ('name', 'rank', 'parent', 'basionym', 'references', 'nsl_url', 'metadata')
    filter_horizontal = ('references',)
    list_display = ('name', 'rank', 'parent', 'nsl_url', 'modified', 'modifier')
    list_filter = ('rank',)
    model_description = 'A scientific name that has been classified into a taxonomic tree.'
    raw_id_fields = ('references',)
    search_fields = ('name', 'rank', 'parent__name', 'basionym__name')
    change_list_template = 'admin/nomenclature/change_list.html'

    def get_queryset(self, request):
        # We can't use ActiveAdminMixin for this model, because the MPTTModel class supercedes
        # the ActiveMixin default manager (i.e. we don't have access to current()).
        qs = super().get_queryset(request)
        # Return 'current' (non-deleted) objects only.
        return qs.filter(effective_to=None)
