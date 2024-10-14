import time
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Simulates the cron job for development purposes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=60,
            help='Time interval in seconds between executions (default: 60 seconds)'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        self.stdout.write(self.style.SUCCESS(f'Starting simulated cron with an interval of {interval} seconds.'))

        try:
            while True:
                # Execute the desired Django command, e.g., 'update'
                self.stdout.write(self.style.WARNING('Running the "update" command...'))
                call_command('update')

                # Wait for the specified interval
                time.sleep(interval)

        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR('Simulation stopped manually.'))
