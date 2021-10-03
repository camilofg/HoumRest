import os
from datetime import datetime
from decimal import Decimal

from django.db.models import Max
from rest_framework import viewsets

from .serializers import PositionSerializer, VisitedPositionsSerializer, SpeedSerializer
from .models import Position
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from . import helpers
from django.contrib.auth.models import User
from configparser import ConfigParser

config = ConfigParser()
ini_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))
config.read(ini_file)


def update_position_time(id_position, current_datetime, visit_duration):
    Position.objects.filter(id=id_position).update(dateModified=current_datetime, visit_duration=visit_duration)


def update_position(id_position, current_datetime):
    Position.objects.filter(id=id_position).update(dateModified=current_datetime)


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        current_datetime = datetime.now()
        if cache.get(data['user']):
            print('get from cache')
            position = cache.get(data['user']).split(',')
            position_start = helpers.PosCoords(data['latitude'], data['longitude'])
            position_end = helpers.PosCoords(Decimal(position[0]), Decimal(position[1]))
            calc_distance = helpers.calc_distance(position_start, position_end).m
            created_date = datetime.strptime(position[2], "%m/%d/%Y %H:%M:%S")
            time_lapse = current_datetime - created_date
            if calc_distance < int(config['DEFAULT']['distance']):
                position_id = Position.objects.filter(user=data['user']).aggregate(Max('id'))['id__max']
                if time_lapse.total_seconds() > int(config['DEFAULT']['time']):
                    update_position_time(position_id, current_datetime, time_lapse.total_seconds())
                else:
                    update_position(position_id, current_datetime)
            else:
                post = Position(user=User.objects.get(id=data['user']),
                                latitude=Decimal(data['latitude']),
                                longitude=Decimal(data['longitude']),
                                dateCreated=current_datetime,
                                dateModified=current_datetime,
                                distance=Decimal(calc_distance),
                                speed=(calc_distance / 1000) / time_lapse.total_seconds() * 3600)
                post.save()
                cache.set(data['user'], str(data['latitude']) + ',' + str(data['longitude']) + ',' +
                          current_datetime.strftime("%m/%d/%Y %H:%M:%S"))
                cache.persist(data['user'])
        else:
            cache.set(data['user'], str(data['latitude']) + ',' + str(data['longitude']) + ',' +
                      current_datetime.strftime("%m/%d/%Y %H:%M:%S"))
            cache.persist(data['user'])
            print('print the cache ttl: ')
            print(cache.ttl(data['user']))
            print('set cache')
            post = Position(user=User.objects.get(id=data['user']),
                            latitude=Decimal(data['latitude']),
                            longitude=Decimal(data['longitude']),
                            dateCreated=current_datetime,
                            dateModified=current_datetime,
                            distance=Decimal(0),
                            speed=Decimal(0))
            post.save()
        return Response(status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        queryset = list(Position.objects.filter(user_id=user_id))
        return queryset


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = VisitedPositionsSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        date_param = self.request.query_params.get('date')
        queryset = list(Position.objects.filter(user_id=user_id, dateCreated__date=date_param)
                        .exclude(visit_duration=Decimal(0)))
        result = [helpers.VisitedPositions(x.latitude, x.longitude,
                                           x.visit_duration) for x in queryset]
        return queryset


class SpeedViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = SpeedSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        speed_param = Decimal(self.request.query_params.get('speed'))
        date_param = self.request.query_params.get('date')
        queryset = [x for x in list(Position.objects.filter(user_id=user_id, dateCreated__date=date_param))
                    if x.speed > speed_param]
        result = [helpers.Speed(x.speed) for x in queryset]
        return queryset
