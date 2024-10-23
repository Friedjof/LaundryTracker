from django.shortcuts import render

from timer.models import Machine

def mock_machines():
    machines: list = []

    for m in Machine.objects.all():
        machines.append({
            'identifier': str(m.identifier),
            'number': int(m.number),
            'name': m.name,
            'type': m.get_type(),
            'status': m.get_status(),
            'time': '45 minutes ago (19:00)',
            'note': 'eg note'
        })

    return machines

def mock_building():
    return 'Demo Building'

def mock_building_description():
    return '<h1>Building Description</h1>'

def mock_building_identifier():
    return '12345678-1234-1234-1234-123456789012'

# Create your views here.
def index(request):
    return render(request, 'laundry/index.html', {
        'title': mock_building(),
        'machines': mock_machines(),
        'building': mock_building(),
        'building_description': mock_building_description(),
        'building_identifier': mock_building_identifier()
    })