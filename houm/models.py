from django.db import models
from django.conf import settings


class Position(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=9)
    longitude = models.DecimalField(max_digits=9, decimal_places=9)
    dateCreated = models.DateTimeField(auto_now_add=True, blank=True, null=False)
    dateModified = models.DateTimeField(auto_now_add=True, blank=True, null=False)
    distance = models.DecimalField(max_digits=9, decimal_places=9)
    speed = models.DecimalField(max_digits=9, decimal_places=9)
    visited = models.BooleanField(default=False)

    def __str__(self):
        return str(self.latitude) + ', ' + str(self.longitude)
