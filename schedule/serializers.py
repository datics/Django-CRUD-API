from rest_framework import serializers
from .models import TimeSlot, Schedule

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'day', 'start_time', 'end_time', 'created_at', 'updated_at']

class ScheduleSerializer(serializers.ModelSerializer):
    time_slot_detail = TimeSlotSerializer(source='time_slot', read_only=True)

    class Meta:
        model = Schedule
        fields = ['id', 'time_slot', 'time_slot_detail', 'external_ids', 'created_at', 'updated_at']

    def validate(self, data):
        if 'external_ids' in data and not isinstance(data['external_ids'], list):
            raise serializers.ValidationError("external_ids must be provided as a list")
        return data
