from decimal import Decimal

import geopy.distance
# from django.contrib.auth.models import User


def calc_distance(coord_start, coord_end):
    coords1 = (float(coord_start.lat), float(coord_start.long))
    coords2 = (float(coord_end.lat), float(coord_end.long))
    distance = geopy.distance.distance(coords1, coords2)
    return distance


class PosCoords:
    def __init__(self, lat: Decimal, long: Decimal):
        self.lat = lat
        self.long = long

    def __str__(self):
        return str(self.lat) + ', ' + str(self.long)


class VisitedPositions(PosCoords):
    def __init__(self, lat: Decimal, long: Decimal, time_spend: Decimal):
        # self.positionCoords = self.positionCoords
        # self.lat = lat
        # self.long = long
        super().__init__(lat, long)
        self.time_spend = time_spend
