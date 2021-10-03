import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Position
from .serializers import PositionSerializer, VisitedPositionsSerializer, SpeedSerializer
import redis


class CreatePositionTestCase(APITestCase):

    def test_create_position(self):
        data = {"user": 1, "latitude": 4.7218901, "longitude": -74.2749591}
        response = self.client.post("/positions/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetVisitsTestCase(APITestCase):

    def test_get_visits(self):
        response = self.client.get("/visits", kwargs={"user_id": 1, "date": "2021-10-03"})
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
