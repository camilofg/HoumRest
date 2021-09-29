from datetime import datetime

from django.db.models import Max
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PositionSerializer
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
            position_end = helpers.PosCoords(float(position[0]), float(position[1]))
            calc_distance = helpers.calc_distance(position_start, position_end)
            print(calc_distance)
            print('position')
            print(position)
            #time_lapse = datetime.now - datetime.strptime(position[2], "%m/%d/%Y %H:%M:%S")
            if (calc_distance * 1000) < 50:
                print('data')
                print(data)
                position_id = Position.objects.filter(user=data['user']).aggregate(Max('id'))['id__max']
                print('positionId')
                print(position_id)
                update_position(position_id, False)#time_lapse.total_seconds() > 600)
            else:
                #time_lapse = datetime.now - datetime.strptime(position[2], "%m/%d/%Y, %H:%M:%S")
                data._mutable = True
                data['user'] = User.objects.get(id=data['user'])
                data['distance'] = calc_distance
                #data['speed'] = distance / time_lapse.total_seconds() * 3600
                post = Position(user=data['user'],
                                latitude=float(data['latitude']),
                                longitude=float(['longitude']),
                                calc_distance=float(calc_distance))
                post.save()
                #Position.objects.create(data)
        else:
            cache.set(data['user'], str(data['latitude']) + ',' + str(data['longitude']) + ',' +
                      datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            print('set cache')
            print(data)
            data._mutable = True
            data['user'] = User.objects.get(id=data['user'])
            post = Position(user=data['user'],
                            latitude=data['latitude'],
                            longitude=data['longitude'],
                            distance=0,
                            speed=0)
            print('post values')
            print(post)
            #post.save()
            Position.objects.create(data)
        print(data)
        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        update_position(data['id'])
        return Response(status=status.HTTP_200_OK)

    def get_queryset(self):
        user_id = self.request.query_params.get('userId')
        queryset = Position.objects.filter(user_id=user_id)
        return queryset
