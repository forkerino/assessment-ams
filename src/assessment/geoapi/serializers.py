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

    def validate_location(self, value):
        lat = value.y
        lon = value.x

        if lat < -90 or lat > 90:
            raise serializers.ValidationError(
                "Invalid latitude, must be between -90 an 90"
            )

        if lon < -180 or lon > 180:
            raise serializers.ValidationError(
                "Invalid longitude, must be between -180 and 180"
            )
        return value
