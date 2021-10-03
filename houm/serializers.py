from rest_framework import serializers

from .helpers import VisitedPositions
from .models import Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'user', 'latitude', 'longitude', 'dateCreated', 'dateModified')
        read_only_fields = ('id',)


class VisitedPositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('user', 'latitude', 'longitude', 'visit_duration')


class SpeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('user', 'latitude', 'longitude', 'speed')
