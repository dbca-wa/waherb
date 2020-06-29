from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib import admin
from nomenclature import urls as nomenclature_urls
from crossreference import urls as crossreference_urls
from naturemap import urls as naturemap_urls
from graphic import urls as graphic_urls

admin.site.site_header = 'WAHerb database administration'
admin.site.index_title = 'WAHerb database'
admin.site.site_title = 'WAHerb'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(nomenclature_urls, namespace='nomenclature')),
    path('', include(crossreference_urls, namespace='crossreference')),
    path('', include(naturemap_urls, namespace='naturemap')),
    path('', include(graphic_urls, namespace='graphic')),
    path('', RedirectView.as_view(pattern_name='admin:index'), name='site_home'),
]
