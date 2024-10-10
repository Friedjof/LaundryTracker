from datetime import datetime
import uuid

from django.db import models

from django.utils import timezone


class Building(models.Model):
    identifier = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    name = models.CharField(max_length=100)

    def get_name(self):
        return f"{self.name}"


# Create your models here.
class Machine(models.Model):
    MACHINE_TYPE = [
        ('W', 'Washer'),
        ('D', 'Dryer'),
    ]

    MACHINE_STATUS = [
        ('A', 'Available'),
        ('R', 'Running'),
        ('F', 'Finished'),
        ('D', 'Defect'),
    ]

    identifier = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    number = models.PositiveIntegerField()

    machine_type = models.CharField(max_length=1, choices=MACHINE_TYPE)
    machine_status = models.CharField(max_length=1, choices=MACHINE_STATUS, default='A')

    timer = models.PositiveIntegerField(default=0)
    timer_start = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(blank=True)
    notes_date = models.DateTimeField(null=True, blank=True)


    def start_timer(self, timer: int = 90):
        self.timer = timer
        self.timer_start = timezone.now()
        self.machine_status = 'R'
        self.save()

    def stop_timer(self):
        self.timer_start = None
        self.machine_status = 'F'
        self.save()

    def remaining_time(self) -> int:
        if self.timer_start is None:
            return 0
        elapsed = timezone.now() - self.timer_start
        remaining = self.timer - elapsed.total_seconds() // 60
        if remaining < 0:
            return 0
        return int(remaining)

    def end_time(self) -> datetime:
        return self.timer_start + timezone.timedelta(minutes=self.timer)

    def update(self):
        if self.machine_status == 'R' and self.remaining_time() == 0:
            self.machine_status = 'F'
            self.save()

    def set_available(self):
        self.machine_status = 'A'
        self.save()

    def _get_building_display(self):
        return self.building.get_name()

    def get_machine_type_display(self):
        return dict(self.MACHINE_TYPE)[self.machine_type]

    def get_notes(self):
        return self.notes

    def set_notes(self, notes: str):
        self.notes = notes
        self.notes_date = timezone.now()
        self.save()

    def set_defect(self):
        self.machine_status = 'D'
        self.save()

    @staticmethod
    def get_building_name(building: str) -> str:
        return Building.objects.get(short_name=building).get_name()

    def __str__(self):
        return f'{self.get_machine_type_display()} ({self.number}) ({self._get_building_display()})'
