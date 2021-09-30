from django.contrib import admin

from .helpers import VisitedPositions
from .models import Position


admin.site.register(Position)
# admin.site.register(VisitedPositions)
