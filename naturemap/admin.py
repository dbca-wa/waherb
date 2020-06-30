from django.contrib import admin
from .models import TaxonLocation
from waherb.utils import WALeafletGeoAdmin


@admin.register(TaxonLocation)
class TaxaLocationAdmin(WALeafletGeoAdmin):
    fields = (
        'name', 'point', 'published_name', 'supra', 'family', 'kingdom', 'conservation_status',
        'vernacular', 'collector', 'collected_date', 'survey', 'source', 'metadata')
    list_display = ('name', 'supra', 'family', 'kingdom', 'vernacular', 'modified', 'modifier')
    list_filter = ('supra', 'kingdom')
    raw_id_fields = ('published_name',)
    search_fields = (
        'name', 'published_name__name', 'supra', 'family', 'kingdom', 'vernacular', 'survey',
        'source__name')
    show_full_result_count = False
