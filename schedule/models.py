from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class TimeSlot(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('day', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.get_day_display()} {self.start_time}-{self.end_time}"

class Schedule(models.Model):
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='schedules')
    external_ids = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Schedule for {self.time_slot}"

    class Meta:
        ordering = ['-created_at']
