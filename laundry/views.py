from django.shortcuts import render

from timer.models import Machine

def mock_machines():
    return Machine.objects.all()

# Create your views here.
def index(request):
    return render(request, 'laundry/index.html', {
        'title': 'Laundry',
        'machines': mock_machines(),
        'building_description': 'This is a building description',
    })