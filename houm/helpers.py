import geopy.distance


def calc_distance(coord_start, coord_end):
    coords1 = (float(coord_start.lat), float(coord_start.long))
    coords2 = (float(coord_end.lat), float(coord_end.long))
    distance = geopy.distance.distance(coords1, coords2)
    return distance


class PosCoords:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    def __str__(self):
        return str(self.lat) + ', ' + str(self.long)
