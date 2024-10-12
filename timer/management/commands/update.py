from datetime import datetime
from django.utils.timezone import get_current_timezone

from django.core.management.base import BaseCommand

from timer.models import Machine
from notifications.tasks import send_machine_finished_notification


class Command(BaseCommand):
    help = 'Update all machines'

    def handle(self, *args, **options):
        updated_count = 0

        for m in Machine.objects.all():
            if m.update():
                send_machine_finished_notification(m)
                updated_count += 1

        current_timezone = get_current_timezone()
        self.stdout.write(self.style.SUCCESS(
            f'[INFO] ({datetime.now(current_timezone).strftime("%Y-%m-%d %H:%M:%S")}) updated {updated_count} machines'))
