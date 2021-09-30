from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'^positions', views.PositionViewSet)
# router.register(r'^visits', views.VisitsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
