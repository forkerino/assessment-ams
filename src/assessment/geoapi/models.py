from django.conf import settings
from django.contrib.gis.db import models as geo_models
from django.db import models


class GeoLocation(models.Model):
    location = geo_models.PointField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
