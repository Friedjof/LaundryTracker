from datetime import datetime
import uuid
import random

from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

from analytics.models import History


# This function returns the default building if it exists, otherwise it creates a dummy building
def get_default_building():
    if Building.objects.exists():
        return Building.objects.first()
    else:
        # Erstelle ein Dummy-Gebäude, falls keines existiert
        return Building.objects.create(name='Demo Building')

def get_default_machine_number():
    default_building = get_default_building()
    if default_building.machine_set.exists():
        return default_building.machine_set.last().number + 1
    else:
        return 1


class Building(models.Model):
    identifier = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True, default='')

    def get_name(self):
        return f"{self.name}"

    def __str__(self):
        return self.get_name()


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
        ('B', 'Blinking'),
        ('U', 'Unknown'),
    ]

    identifier = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    building = models.ForeignKey(Building, on_delete=models.CASCADE, default=get_default_building)
    number = models.PositiveIntegerField(default=get_default_machine_number)
    name = models.CharField(max_length=8, blank=True)

    machine_type = models.CharField(max_length=1, choices=MACHINE_TYPE, default='W')
    machine_status = models.CharField(max_length=1, choices=MACHINE_STATUS, default='A')

    timer = models.PositiveIntegerField(default=0)
    timer_start = models.DateTimeField(default=timezone.now)

    notes = models.TextField(blank=True)
    notes_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None, **kwargs):
        if not self.name:
            self.name = f'{self.number}'

        History.snapshot(self)

        super().save(*args, force_insert, force_update, using, update_fields, **kwargs)

    def start_timer(self, timer: int = 90):
        self.timer = timer
        self.timer_start = timezone.now()
        self.machine_status = 'R'
        self.save()

    def remaining_time(self) -> int:
        if self.timer_start is None:
            return 0

        remaining = self.timer - (timezone.now() - self.timer_start).total_seconds() // 60

        if remaining < 0:
            return 0
        return int(remaining)

    def elapsed_time(self) -> int:
        return (timezone.now() - self.timer_start).total_seconds() // 60

    def end_time(self) -> datetime:
        return self.timer_start + timezone.timedelta(minutes=self.timer)

    def update(self) -> bool:
        if self.machine_status == 'R' and self.remaining_time() == 0:
            self.machine_status = 'F'
            self.timer = 0
            self.timer_start = timezone.now()
            self.save()

            return True
        elif self.machine_status == 'B' and self.remaining_time() == 0:
            self.machine_status = 'A'
            self.timer = 0
            self.timer_start = timezone.now()
            self.save()

            return True
        elif self.machine_status == 'F' and self.elapsed_time() > 120:
            self.machine_status = 'A'
            self.timer = 0
            self.timer_start = timezone.now()
            self.save()

            return True
        return False

    def _get_building_display(self):
        return self.building.get_name()

    def get_machine_type_display(self):
        return dict(self.MACHINE_TYPE)[self.machine_type]

    def get_status(self):
        return dict(self.MACHINE_STATUS)[self.machine_status]

    def get_type(self):
        return dict(self.MACHINE_TYPE)[self.machine_type]

    def get_time_note(self) -> str:
        rt = self.timer - (timezone.now() - self.timer_start).total_seconds() / 60

        if int(rt) == 0:
            return 'right now'
        elif rt < 0:
            rt = abs(rt)

            if rt < 120:
                return f'{rt:.0f}min ago'
            elif rt < 1440:
                hours = rt // 60
                minutes = rt % 60
                if minutes == 0:
                    return f'{hours:.0f}h ago'
                return f'{hours:.0f}h and {minutes:.0f}min ago'
            else:
                days = rt // 1440
                hours = (rt % 1440) // 60
                if hours == 0:
                    return f'{days:.0f}d ago'
                return f'{days:.0f}d and {hours:.0f}h ago'
        else:
            if rt < 120:
                return f'{rt:.0f}min remaining'
            elif rt < 1440:
                hours = rt // 60
                minutes = rt % 60
                if minutes == 0:
                    return f'{hours:.0f}h remaining'
                return f'{hours:.0f}h and {minutes:.0f}min remaining'
            else:
                days = rt // 1440
                hours = (rt % 1440) // 60
                if hours == 0:
                    return f'{days:.0f}d remaining'
                return f'{days:.0f}d and {hours:.0f}h remaining'

    def get_notes(self):
        return self.notes

    def set_notes(self, notes: str = ''):
        self.notes = notes
        self.notes_date = timezone.now()
        self.save()

    def set_defect(self, notes: str = None):
        if notes:
            self.notes = notes
            self.notes_date = timezone.now()
        self.machine_status = 'D'
        self.timer_start = timezone.now()
        self.timer = 0
        self.save()

    def set_available(self) -> bool:
        if self.machine_status != 'A':
            self.machine_status = 'A'
            self.timer_start = timezone.now()
            self.timer = 0
            self.save()

            return True
        return False

    def set_blinking(self):
        if self.machine_status == 'B':
            self.machine_status = 'A'
            self.timer = 0
            self.timer_start = timezone.now()
            self.save()
        else:
            self.machine_status = 'B'
            self.timer = 8 * 60 # 8 hours
            self.timer_start = timezone.now()
            self.save()

    def set_finished(self):
        self.machine_status = 'F'
        self.timer = 0
        self.timer_start = timezone.now()
        self.save()

    def set_unchanged(self):
        if self.machine_status == 'A':
            self.timer = 0
            self.timer_start = timezone.now()
            self.save()
        elif self.machine_status == 'R':
            r = self.remaining_time()
            self.timer = r
            self.timer_start = timezone.now() - timezone.timedelta(minutes=r)
            self.save()
        elif self.machine_status == 'D':
            self.timer = 0
            self.timer_start = timezone.now()
            self.save()
        elif self.machine_status == 'B':
            r = self.remaining_time()
            self.timer = r
            self.timer_start = timezone.now() - timezone.timedelta(minutes=r)
            self.save()
        else:
            self.machine_status = 'U'
            self.timer = 0
            self.timer_start = timezone.now()
            self.save()

    @staticmethod
    def get_longest_unused_machine(building: uuid.UUID) -> 'Machine' or None:
        machines = Machine.objects.filter(building=building, timer_start__lt=(timezone.now() - timezone.timedelta(hours=12))).order_by('timer_start')

        if machines.exists():
            return random.choice(machines)
        return None

    @staticmethod
    def get_building_name(building: str) -> str:
        return Building.objects.get(short_name=building).get_name()

    def snapshot(self):
        History.snapshot(self)

    def __str__(self):
        return f'{self.get_machine_type_display()} ({self.name}) ({self._get_building_display()})'

    def __repr__(self):
        return f'{self.get_machine_type_display()} ({self.name}) ({self._get_building_display()})'

    def as_dict(self):
        return {
            'identifier': str(self.identifier),
            'number': int(self.number),
            'name': self.name,
            'type': self.get_type(),
            'status': self.get_status(),
            'time': self.get_time_note(),
            'notes': self.get_notes()
        }

    class Meta:
        unique_together = ['building', 'number']
        ordering = ['building', 'number']


class BuildingAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} for {self.building}'

    class Meta:
        unique_together = ['user', 'building']
        ordering = ['user', 'building']
