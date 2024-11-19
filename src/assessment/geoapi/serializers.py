from .models import GeoLocation
from django.contrib.auth.models import User
from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers


class GeoLocationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )
    location = PointField(required=True, srid=4326)

    class Meta:
        model = GeoLocation
        fields = ["id", "user", "location", "timestamp"]
