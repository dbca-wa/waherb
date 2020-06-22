from django.urls import path
from .views import TaxonTreeView

app_name = 'nomenclature'
urlpatterns = [
    path('api/taxon-tree/<int:pk>/', TaxonTreeView.as_view(), name='taxon_tree'),
]
