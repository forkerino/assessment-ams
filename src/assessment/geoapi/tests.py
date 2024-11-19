from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase

from .models import GeoLocation
from .views import GeoLocationViewset
from rest_framework.test import APIRequestFactory, force_authenticate


class GeoLocationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="John", email="john@john.com")
        GeoLocation.objects.create(
            location=GEOSGeometry("POINT(4.8 52.6)"), user=self.user
        )
        GeoLocation.objects.create(location=GEOSGeometry("POINT(4.7 52.5)"), user=None)

    def test_geo_location_has_x_and_y(self):
        point = GeoLocation.objects.first()
        self.assertIsNotNone(point.location.x)
        self.assertIsNotNone(point.location.y)

    def test_geo_location_can_be_filtered_on_user(self):
        points = GeoLocation.objects.filter(user=self.user)
        self.assertTrue(len(points) == 1)

    def test_geo_location_has_automatic_timestamp(self):
        points = GeoLocation.objects.all()
        self.assertTrue(points[0].timestamp < points[1].timestamp)


class GeoLocationApiTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory(enforce_csrf_checks=True)
        self.admin = User.objects.create(
            username="Joe", email="joe@joe.com", is_superuser=True
        )
        self.user = User.objects.create(username="John", email="john@john.com")
        self.view = GeoLocationViewset.as_view({"get": "list", "post": "create"})
        GeoLocation.objects.create(
            location=GEOSGeometry("POINT(4.8 52.6)"), user=self.user
        )
        GeoLocation.objects.create(
            location=GEOSGeometry("POINT(4.7 52.5)"), user=self.admin
        )

    def test_can_create_geo_location_without_user(self):
        self.factory.post(
            "/geolocations/",
            {"location": {"latitude": 52, "longitude": 5}, "user": None},
            format="json",
        )
        point = GeoLocation.objects.filter(user=None)
        self.assertIsNotNone(point)

    def test_can_list_all_points_for_superuser(self):
        request = self.factory.get("/geolocations/")
        force_authenticate(request, user=self.admin)
        response = self.view(request)
        ### etc.

    def test_can_list_users_points(self):
        pass

    def test_can_list_points_without_user_if_unauthorized(self):
        pass
