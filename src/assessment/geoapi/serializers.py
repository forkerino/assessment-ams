from .models import GeoLocation
from rest_framework import serializers

class GeoLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoLocation
        fields = ['location', 'timestamp', 'user']
