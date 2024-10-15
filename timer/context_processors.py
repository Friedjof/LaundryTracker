def version_context_processor(request):
    from django.conf import settings
    return {
        'VERSION': settings.VERSION,  # Die Versionsnummer aus settings.py
    }
