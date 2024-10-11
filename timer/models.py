from datetime import datetime
import uuid

from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


class Building(models.Model):
    identifier = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    name = models.CharField(max_length=100)

    def get_name(self):
        return f"{self.name}"

    def __str__(self):
        return self.get_name()


# This function returns the default building if it exists, otherwise it creates a dummy building
def get_default_building():
    if Building.objects.exists():
        return Building.objects.first()
    else:
        # Erstelle ein Dummy-Gebäude, falls keines existiert
        return Building.objects.create(name='Default Building')

def get_default_machine_number():
    if Machine.objects.exists():
        return Machine.objects.last().number + 1
    else:
        return 1


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

    building = models.ForeignKey(Building, on_delete=models.CASCADE, default=get_default_building)

    number = models.PositiveIntegerField(default=get_default_machine_number)

    machine_type = models.CharField(max_length=1, choices=MACHINE_TYPE)
    machine_status = models.CharField(max_length=1, choices=MACHINE_STATUS, default='A')

    timer = models.PositiveIntegerField(default=0)
    timer_start = models.DateTimeField(default=timezone.now)

    notes = models.TextField(blank=True)
    notes_date = models.DateTimeField(default=timezone.now)


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

        remaining = self.timer - (timezone.now() - self.timer_start).total_seconds() // 60
        if remaining < 0:
            return 0
        return int(remaining)

    def end_time(self) -> datetime:
        return self.timer_start + timezone.timedelta(minutes=self.timer)

    def update(self) -> bool:
        if self.machine_status == 'R' and self.remaining_time() == 0:
            self.machine_status = 'F'
            self.save()

            return True
        return False

    def set_available(self) -> bool:
        if self.machine_status != 'A':
            self.machine_status = 'A'
            self.timer_start = timezone.now()
            self.save()

            return True
        return False

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

    def __repr__(self):
        return f'{self.get_machine_type_display()} ({self.number}) ({self._get_building_display()})'

    class Meta:
        unique_together = ['building', 'number']
        ordering = ['building', 'number']
