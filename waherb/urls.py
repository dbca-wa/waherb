from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib import admin
from nomenclature import urls as nomenclature_urls

admin.site.site_header = 'WAHerb database administration'
admin.site.index_title = 'WAHerb database'
admin.site.site_title = 'WAHerb'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(nomenclature_urls, namespace='nomenclature')),
    path('', RedirectView.as_view(pattern_name='admin:index'), name='site_home'),
]
