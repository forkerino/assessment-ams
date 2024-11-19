from .models import GeoLocation
from .serializers import GeoLocationSerializer
from rest_framework import viewsets

class GeoLocationViewset(viewsets.ModelViewSet):
    queryset = GeoLocation.objects.all()
    serializer_class = GeoLocationSerializer
