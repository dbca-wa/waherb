"use strict";

// NOTE: the following global variables need to be set prior to loading this script:
// * geoserver_wms_url
// Define tile layers.
var landgateOrthomosaic = L.tileLayer.wms(
  geoserver_wms_url,
  {
    crs: L.CRS.EPSG4326,
    layers: 'landgate:virtual_mosaic',
    tileSize: 1024,
    format: 'image/jpeg',
    tiled: true,
    version: '1.1.1',
  }
);
var mapboxStreets = L.tileLayer.wms(
  geoserver_wms_url,
  {
    crs: L.CRS.EPSG4326,
    layers: 'dbca:mapbox-streets',
    tileSize: 1024,
    format: 'image/jpeg',
    tiled: true,
    version: '1.1.1',
  }
);
var dbcaLands = L.tileLayer.wms(
  geoserver_wms_url,
  {
    crs: L.CRS.EPSG4326,
    layers: 'cddp:legislated_lands_and_waters',
    opacity: 0.75,
    tileSize: 1024,
    format: 'image/png',
    tiled: true,
    transparent: true,
    version: '1.1.1',
  }
);
var miningTenements = L.tileLayer.wms(
  "https://services.slip.wa.gov.au/public/services/SLIP_Public_Services/Industry_and_Mining/MapServer/WMSServer",
  {
    crs: L.CRS.EPSG4326,
    layers: '20',
    opacity: 0.75,
    tileSize: 1024,
    format: 'image/png',
    tiled: true,
    transparent: true,
    version: '1.1.1',
  }
);
var empty = L.tileLayer('');

// Define map.
var map = L.map('map', {
  crs: L.CRS.EPSG4326,
  center: [-31.96, 115.87],
  zoom: 5,
  layers: [mapboxStreets],  // Sets default selections.
});

// Define layer groups.
var baseMaps = {
  "Landgate Orthomosaic": landgateOrthomosaic,
  "OpenStreetMap Streets": mapboxStreets,
  "No base layer": empty,
};
var overlayMaps = {
  "DBCA tenure": dbcaLands,
  "Mining tenements": miningTenements,
};

// Define layer control.
L.control.layers(baseMaps, overlayMaps).addTo(map);

// Define scale bar
L.control.scale({maxWidth: 500, imperial: false}).addTo(map);

// Add a feature group to the map to contain sample markers.
//var samples = new L.featureGroup();
var samples = new L.markerClusterGroup({
  maxClusterRadius: 50,
});
map.addLayer(samples);

// Function to generate WKT from a Leaflet layer.
// Reference: https://gist.github.com/bmcbride/4248238
function toWKT (layer) {
  var lng, lat, coords = [];
  if (layer instanceof L.Polygon || layer instanceof L.Polyline) {
    var latlngs = layer.getLatLngs();
  for (var i = 0; i < latlngs.length; i++) {
    var latlngs1 = latlngs[i];
    if (latlngs1.length){
    for (var j = 0; j < latlngs1.length; j++) {
      coords.push(latlngs1[j].lng + " " + latlngs1[j].lat);
      if (j === 0) {
        lng = latlngs1[j].lng;
        lat = latlngs1[j].lat;
      }
    }}
    else
    {
      coords.push(latlngs[i].lng + " " + latlngs[i].lat);
      if (i === 0) {
        lng = latlngs[i].lng;
        lat = latlngs[i].lat;
      }
    }
  }
    if (layer instanceof L.Polygon) {
      return "POLYGON((" + coords.join(",") + "," + lng + " " + lat + "))";
    } else if (layer instanceof L.Polyline) {
      return "LINESTRING(" + coords.join(",") + ")";
    }
  } else if (layer instanceof L.Marker) {
    return "POINT(" + layer.getLatLng().lng + " " + layer.getLatLng().lat + ")";
  }
}

// Global variable to store API response data.
var ids;

// Function to draw passed-in array of points on the samples feature group.
var mapSamples = function(data) {
  ids = [];
  samples.clearLayers();
  // Iterate through the array and add markers for each point.
  data.forEach((element) => {
    ids.push(element.id);
    var marker = L.marker(
        // Leaflet.marker wants coords as LatLon (Y,X) :\
        [element.lat, element.lon],
      {
        title: element.name,
        clickable: false,
      }
    );
    marker.addTo(samples);
  });
  map.fitBounds(samples.getBounds());
};

// Add a feature group to store drawn features.
var drawnItems = new L.featureGroup();
map.addLayer(drawnItems);
var drawControl = new L.Control.Draw({
  draw: {
    polyline: false,
    polygon: {
      allowIntersection: false, // Restricts shapes to simple polygons
      drawError: {
        color: '#e1e100',
        message: 'Unable to draw intersecting polygons',
      },
    },
    circlemarker: false,
    marker: false,
  },
  edit: {
    featureGroup: drawnItems,
    remove: false,
    edit: false,
  },
});
map.addControl(drawControl);

map.on(L.Draw.Event.CREATED, function (e) {
  $("div#api-response").html("<p>Querying database...</p>");
  $('#download-button').prop('disabled', true);
  drawnItems.clearLayers();
  var type = e.layerType, layer = e.layer;
  if (type === 'circle') {
    let point = `${layer._latlng.lng},${layer._latlng.lat}`;
    var radius = layer.getRadius();
    if (radius > 20000) {
      alert('NOTE: search radius will be limited to 20 km from origin');
      radius = 20000;
    }
    $.getJSON("/naturemap/api/area/", {point: point, r: radius}, function(data) {
      $("div#api-response").html(`<p>${data.length} results returned</p>`);
      if (data.length > 0) {
        mapSamples(data);
        $('#download-button').data('search', 'area');
        $('#download-button').prop('disabled', false);
      }
    });
  } else if (type === 'polygon' || type === 'rectangle') {
    let poly = toWKT(layer);
    $.getJSON("/naturemap/api/area/", {poly: poly}, function(data) {
      $("div#api-response").html(`<p>${data.length} results returned</p>`);
      if (data.length > 0) {
        mapSamples(data);
        $('#download-button').data('search', 'area');
        $('#download-button').prop('disabled', false);
      }
    });
  }
  drawnItems.addLayer(layer);
});

// Document onready events
$(function() {
  $('#download-button').prop('disabled', true);
  var cache = {};  // Short-lived page cache of API requests/responses.

  $('#species-name').autocomplete({
    delay: 500,
    minLength: 3,
    source: function(request, resp) {
      var term = request.term;
      if (term in cache) {
          resp(cache[term]);
          return;
      }
      $.getJSON("/naturemap/api/name/", {q: request.term}, function(data) {
        data = data.sort();
        cache[term] = data;
        resp(data);
      })
    },
  });

  $('#species-name-form').on('submit', function(e) {
    e.preventDefault(); // Interrupt the form submit.
    $('#download-button').prop('disabled', true);
    $("div#api-response").html("<p>Querying database...</p>");
    var name = $("input#species-name").val();
    $.getJSON("/naturemap/api/name/", {name: name}, function(data) {
      $("div#api-response").html(`<p>${data.length} results returned</p>`);
      if (data.length > 0) {
        mapSamples(data);
        $('#download-button').data('search', 'name');
        $('#download-button').prop('disabled', false);
      }
    });
  });

  $('#download-button').click(function() {
    if ($('#download-button').data('search') === 'name') {
      // We searched on name
      var name = $("input#species-name").val();
      window.open("/naturemap/api/name/?download=&name=" + name);
    } else if ($('#download-button').data('search') === 'area') {
      // We searched on area.
      window.open("/naturemap/api/area/?download=&ids=" + ids.join(","));
    }
  });

});
