import django.db.utils
from background_task import background

from .models import Machine


@background(schedule=5)
def update_machine_status():
    machines = Machine.objects.filter(machine_status='R')
    for machine in machines:
        machine.update()


# hint from https://github.com/django-background-tasks/django-background-tasks/issues/205
try:
    update_machine_status(repeat=5, repeat_until=None)
except django.db.utils.OperationalError:
    print('Database not ready yet')
