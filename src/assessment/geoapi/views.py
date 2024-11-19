from .models import GeoLocation
from .serializers import GeoLocationSerializer
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Q
from rest_framework import viewsets


class GeoLocationViewset(viewsets.ModelViewSet):
    queryset = GeoLocation.objects.all()
    serializer_class = GeoLocationSerializer

    def get_queryset(self):
        objects = GeoLocation.objects
        user = self.request.user

        # Anonymous users can only see points without a user
        if user.is_anonymous:
            objects = objects.filter(user__isnull=True)

        # Authenticated users can only see their own points, unless they are a superuser
        if not user.is_superuser and user.is_authenticated:
            objects = objects.filter(Q(user=user) | Q(user__isnull=True))

        # Filter on lat/lon/(maximum) distance
        params = self.request.query_params
        lat = params.get("lat")
        lon = params.get("lon")
        distance = params.get("distance")
        if distance and lat and lon:
            origin = GEOSGeometry(f"POINT({lon} {lat})", srid=4326)
            objects = objects.annotate(
                distance=Distance("location", origin, srid=4326)
            ).filter(distance__lte=distance)

        return objects.all()
