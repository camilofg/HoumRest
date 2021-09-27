from rest_framework import serializers
from .models import Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'user', 'latitude', 'longitude', 'dateCreated', 'dateModified')
        read_only_fields = ('id',)
