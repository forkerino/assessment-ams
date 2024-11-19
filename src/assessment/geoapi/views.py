from .models import GeoLocation
from .serializers import GeoLocationSerializer
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import viewsets


class GeoLocationViewset(viewsets.ModelViewSet):
    queryset = GeoLocation.objects.all()
    serializer_class = GeoLocationSerializer

    def get_queryset(self):
        objects = GeoLocation.objects.all()
        params = self.request.query_params
        lat = params.get("lat")
        lon = params.get("lon")
        distance = params.get("distance")
        if distance and lat and lon:
            origin = GEOSGeometry(f"POINT({lon} {lat})", srid=4326)
            return objects.annotate(
                distance=Distance("location", origin, srid=4326)
            ).filter(distance__lte=distance)
        return objects
