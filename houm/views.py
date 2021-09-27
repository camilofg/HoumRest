from datetime import datetime

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PositionSerializer
from .models import Position
from rest_framework.response import Response
from rest_framework import status


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def update(self, request, *args, **kwargs):
        data = request.data
        Position.objects.filter(id=data['id']).update(dateModified=datetime.now())
        return Response(status=status.HTTP_200_OK)

    def get_queryset(self):
        user_id = self.request.query_params.get('userId')
        queryset = Position.objects.filter(user_id=user_id)
        return queryset
