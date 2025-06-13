from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'time-slots', views.TimeSlotViewSet)
router.register(r'schedules', views.ScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
