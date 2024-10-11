from django.core.management.base import BaseCommand
from background_task.models import CompletedTask, Task
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Clear old background tasks'
    _older_than = 10 # in minutes

    def handle(self, *args, **kwargs):
        time_threshold = timezone.now() - timedelta(minutes=self._older_than)

        # Clear completed tasks older than 10 minutes
        CompletedTask.objects.filter(locked_at__lt=time_threshold).delete()

        # Clear tasks older than 10 minutes
        Task.objects.filter(locked_at__lt=time_threshold).delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully cleared old background tasks (older than {self._older_than} minutes)'))
