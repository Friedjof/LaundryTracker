import uuid

from django.db import models
from django.utils import timezone


# Create your models here.
class History(models.Model):
    MACHINE_STATUS = (
        ('A', 'Available'),
        ('R', 'Running'),
        ('F', 'Finished'),
        ('D', 'Defect'),
        ('B', 'Blinking'),
        ('U', 'Unknown'),
    )

    MACHINE_TYPE = (
        ('W', 'Washer'),
        ('D', 'Dryer'),
    )

    identifier = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    building_identifier = models.UUIDField(editable=False)
    building = models.CharField(max_length=100, editable=False)
    machine_identifier = models.UUIDField(editable=False)
    machine_type = models.CharField(max_length=100, editable=False, choices=MACHINE_TYPE)
    machine_status = models.CharField(max_length=100, editable=False, choices=MACHINE_STATUS)
    machine_number = models.IntegerField(editable=False, default=0)
    timer = models.IntegerField(editable=False)
    timer_start = models.DateTimeField(editable=False)
    notes = models.TextField(editable=False)
    notes_date = models.DateTimeField(editable=False)

    def __str__(self):
        return f"{self.created_at}"

    @staticmethod
    def snapshot(machine):
        History.objects.create(
            identifier=uuid.uuid4(),
            building_identifier=str(machine.building.identifier),
            building=machine.building.name,
            machine_identifier=str(machine.identifier),
            machine_type=machine.machine_type,
            machine_status=machine.machine_status,
            machine_number=machine.number,
            timer=machine.timer,
            timer_start=machine.timer_start,
            notes=machine.notes,
            notes_date=machine.notes_date,
        )
