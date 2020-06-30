from django.urls import path
from .views import TaxonLocationSearch, TaxonLocationNameAPI, TaxonLocationAreaAPI


app_name = 'crossreference'
urlpatterns = [
    path('naturemap/api/name/', TaxonLocationNameAPI.as_view(), name='api_taxonlocation_name'),
    path('naturemap/api/area/', TaxonLocationAreaAPI.as_view(), name='api_taxonlocation_area'),
    path('naturemap/', TaxonLocationSearch.as_view(), name='taxonlocation_search'),
]
