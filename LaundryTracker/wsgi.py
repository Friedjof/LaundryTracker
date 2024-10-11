"""
WSGI config for LaundryTracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LaundryTracker.settings')

# Import and run the command
from django.core.management import call_command
call_command('clear_old_tasks')

application = get_wsgi_application()