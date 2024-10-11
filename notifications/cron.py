from django_cron import CronJobBase, Schedule
from django.utils import timezone

from background_task.models import CompletedTask, Task
from datetime import timedelta


class ClearBackgroundTasksCronJob(CronJobBase):
    RUN_EVERY_MINS = 15

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'notifications.clear_background_tasks'

    def do(self):
        time_threshold = timezone.now() - timedelta(minutes=self.RUN_EVERY_MINS)

        CompletedTask.objects.filter(locked_at__lt=time_threshold).delete()

        Task.objects.filter(locked_at__lt=time_threshold).delete()

        print(f'[INFO] Old tasks cleared at {timezone.now()}')
