from datetime import datetime
from decimal import Decimal

from django.db.models import Max
# from django.shortcuts import render
from rest_framework import viewsets

from .helpers import VisitedPositions
from .serializers import PositionSerializer, VisitedPositionsSerializer
from .models import Position
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from . import helpers
from django.contrib.auth.models import User

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def update_position(id_position, visited):
    Position.objects.filter(id=id_position).update(dateModified=datetime.now(), visited=visited)


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if cache.get(data['user']):
            print('get from cache')
            position = cache.get(data['user']).split(',')
            position_start = helpers.PosCoords(data['latitude'], data['longitude'])
            position_end = helpers.PosCoords(Decimal(position[0]), Decimal(position[1]))
            calc_distance = helpers.calc_distance(position_start, position_end).m
            time_lapse = datetime.now() - datetime.strptime(position[2], "%m/%d/%Y %H:%M:%S")
            if calc_distance < 50:
                position_id = Position.objects.filter(user=data['user']).aggregate(Max('id'))['id__max']
                update_position(position_id, time_lapse.total_seconds() > 60)
            else:
                post = Position(user=User.objects.get(id=data['user']),
                                latitude=Decimal(data['latitude']),
                                longitude=Decimal(data['longitude']),
                                distance=Decimal(calc_distance),
                                speed=(calc_distance/1000) / time_lapse.total_seconds() * 3600)
                post.save()
        else:
            cache.set(data['user'], str(data['latitude']) + ',' + str(data['longitude']) + ',' +
                      datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            print('set cache')
            post = Position(user=User.objects.get(id=data['user']),
                            latitude=Decimal(data['latitude']),
                            longitude=Decimal(data['longitude']),
                            distance=Decimal(0),
                            speed=Decimal(0))
            post.save()
        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        update_position(data['id'])
        return Response(status=status.HTTP_200_OK)

    def get_queryset(self):
        # self.serializer_class = VisitedPositionsSerializer
        user_id = self.request.query_params.get('userId')
        queryset = list(Position.objects.filter(user_id=user_id, visited=True))
        # result = map(lambda x: helpers.VisitedPositions(x.latitude, x.longitude, 0), queryset)
        result = [helpers.VisitedPositions(x.latitude, x.longitude,
                                           (x.dateCreated - x.dateModified).total_seconds()/3600) for x in queryset]
        return queryset
        # Response(helpers.VisitedPositions(4.723453, -72.543455, 89))
