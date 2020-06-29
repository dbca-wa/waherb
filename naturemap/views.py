from datetime import datetime
from django.core.serializers import serialize
from django.conf import settings
from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.views.generic import View, TemplateView
from .models import TaxonLocation


class TaxonLocationNameAPI(View):
    """Lightweight API endpoint to query TaxonLocation objects based upon name.
    """
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        # If we're downloading, make use of the Django ORM (slower) so that we can alse use the
        # serialise function to generate GeoJSON.
        if 'download' in request.GET:
            # Queryset filter based on passed in param `name` (assumes exact, case-insenstive match):
            if 'name' in request.GET and request.GET['name']:
                name = request.GET['name']
                objects = TaxonLocation.objects.filter(name__icontains=name)
                data = serialize('geojson', objects, geometry_field='point', fields=('name',))
                resp = HttpResponse(data, content_type='application/json')
                resp['Content-Disposition'] = 'attachment; filename="{}_{}.geojson"'.format(name.replace(' ', '_').lower(), datetime.now().isoformat())
                return resp

        # If we're not downloading, bypass the Django ORM for performance.
        # NOTE: using ILIKE in the WHERE clause uses the Gin index on the name field (using = does not).
        # Query unique names based on passed-in param `q`:
        if 'q' in request.GET and request.GET['q']:
            cursor = connection.cursor()
            sql = """SELECT DISTINCT name
            FROM naturemap_taxonlocation
            WHERE name ILIKE '%%{}%%'""".format(request.GET['q'])
            cursor.execute(sql)
            rows = [row[0] for row in cursor.fetchall()]
        # Query sample points based on passed in param `name` (assumes exact, case-insenstive match):
        elif 'name' in request.GET and request.GET['name']:
            name = request.GET['name']
            cursor = connection.cursor()
            sql = """SELECT id, name, ST_X(point), ST_Y(point)
            FROM naturemap_taxonlocation
            WHERE name ILIKE '{}%%'""".format(name)
            cursor.execute(sql)
            rows = [{'id': row[0], 'name': row[1], 'lon': row[2], 'lat': row[3]} for row in cursor.fetchall()]
        else:
            rows = []

        return JsonResponse(rows, safe=False)


class TaxonLocationAreaAPI(View):
    """API endpoint to equery TaxonLocation objects based on spatial area.
    Area can be supplied as a buffered point (point, radius in metres) or as a polygon (WKT).
    """
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        # If we're downloading, make use of the Django ORM (slower) so that we can alse use the
        # serialise function to generate GeoJSON.
        if 'download' in request.GET:
            # TODO: parse spatial queries.
            if 'ids' in request.GET and request.GET['ids']:
                ids = request.GET['ids'].split(',')
                objects = TaxonLocation.objects.filter(id__in=ids)
                data = serialize('geojson', objects, geometry_field='point', fields=('name',))
                resp = HttpResponse(data, content_type='application/json')
                resp['Content-Disposition'] = 'attachment; filename="taxon_locations_{}.geojson"'.format(datetime.now().isoformat())
                return resp

        # Query by point and radius:
        if 'point' in request.GET and request.GET['point']:
            point = request.GET['point']  # Point having format LON,LAT (GDA94/EPSG 4283 assumed).
            if 'r' in request.GET and request.GET['r']:
                r = float(request.GET['r'])  # Radius in metres.
            else:
                r = 100.0
            sql = """SELECT id, name, ST_X(point), ST_Y(point)
            FROM naturemap_taxonlocation
            WHERE ST_DWithin(geography(point), ST_SetSRID(ST_MakePoint({}), 4283), {})""".format(point, r)
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = [{'id': row[0], 'name': row[1], 'lon': row[2], 'lat': row[3]} for row in cursor.fetchall()]
        # Query by area:
        elif 'poly' in request.GET and request.GET['poly']:
            poly = request.GET['poly']  # WKT string of a polygon (GDA94/EPSG 4283 assumed).
            sql = """SELECT id, name, ST_X(point), ST_Y(point)
            FROM naturemap_taxonlocation
            WHERE ST_Within(point, ST_GeomFromText('{}', 4283))""".format(poly)
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = [{'id': row[0], 'name': row[1], 'lon': row[2], 'lat': row[3]} for row in cursor.fetchall()]
        else:
            rows = []

        return JsonResponse(rows, safe=False)


class TaxonLocationSearch(TemplateView):
    template_name = 'naturemap/taxonlocation_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GEOSERVER_WMS_URL'] = settings.GEOSERVER_WMS_URL
        return context
