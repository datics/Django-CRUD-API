from datetime import datetime

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from .models import TimeSlot, Schedule
from .serializers import TimeSlotSerializer, ScheduleSerializer


class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_weekly_schedule(self, request):
        """
        Get the complete weekly schedule grouped by day
        """
        weekly_schedule = {}
        for day in TimeSlot.DAY_CHOICES:
            day_name = day[0]
            time_slots = TimeSlot.objects.filter(day=day_name)
            weekly_schedule[day_name] = []
            
            for time_slot in time_slots:
                schedule = time_slot.schedules.first()
                if schedule:
                    weekly_schedule[day_name].append({
                        'start': time_slot.start_time.strftime('%H:%M'),
                        'stop': time_slot.end_time.strftime('%H:%M'),
                        'external_ids': schedule.external_ids
                    })
        
        return Response({"schedule": weekly_schedule})

    @action(detail=False, methods=['post'])
    def set_weekly_schedule(self, request):
        """
        Accepts a JSON payload in the same structure returned by `get_weekly_schedule` and
        bulk-creates/updates `TimeSlot` and `Schedule` records.

        Example payload::

            {
              "schedule": {
                "monday": [
                  {"start": "00:00", "stop": "01:00", "ids": [1, 2]}
                ],
                "tuesday": []
              }
            }
        """
        data = request.data.get('schedule')
        if not isinstance(data, dict):
            return Response({'detail': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)

        created, updated = 0, 0
        for day, slots in data.items():
            if not isinstance(slots, list):
                continue
            for slot in slots:
                ids = slot.get('external_ids') or slot.get('ids') or slot.get('camera_ids') or []
                try:
                    start_time = datetime.strptime(slot['start'], '%H:%M').time()
                    end_time = datetime.strptime(slot['stop'], '%H:%M').time()
                except (KeyError, ValueError):
                    continue

                time_slot, _ = TimeSlot.objects.get_or_create(
                    day=day.lower(), start_time=start_time, end_time=end_time
                )
                sch_obj, created_flag = Schedule.objects.update_or_create(
                    time_slot=time_slot,
                    defaults={'external_ids': ids}
                )
                if created_flag:
                    created += 1
                else:
                    updated += 1

        return Response({'created': created, 'updated': updated})

    @action(detail=False, methods=['get'], url_path='time-slot-list')
    def time_slot_list(self, request):
        """Return a flat list of all `TimeSlot` objects."""
        slots = TimeSlot.objects.all().order_by('day', 'start_time')
        serializer = TimeSlotSerializer(slots, many=True)
        return Response(serializer.data)
    

    @action(detail=False, methods=['put'],
            url_path=r'update-time-slot',
            permission_classes=[permissions.IsAuthenticated])
    def update_time_slot(self, request):
        instance = get_object_or_404(TimeSlot, pk=request.data['id'])
        serializer = TimeSlotSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    @action(detail=False, methods=['put'],
            url_path=r'update-weekly-schedule',
            permission_classes=[permissions.IsAuthenticated])
    def update_weekly_schedule(self, request):
        instance = get_object_or_404(Schedule, pk=request.data['id'])
        serializer = ScheduleSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
