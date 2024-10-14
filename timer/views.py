from datetime import datetime

import markdown
import bleach

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render

from .models import Machine, Building

from notifications.tasks import send_machine_available_notification, send_machine_finished_notification


def index(request, building):
    try:
        building = Building.objects.get(identifier=building)
    except ObjectDoesNotExist:
        return render(request, 'timer/404.html', {'year': datetime.now().year}, status=404)

    if request.method == 'POST':
        # POST-Request: Aktuellen Maschinenstatus als JSON zurückgeben
        machines = Machine.objects.filter(building=building)
        machines_data = []

        # Update all machines
        for m in machines:
            if m.update():
                if m.machine_status == 'F':
                    send_machine_finished_notification(m)

            machines_data.append({
                'identifier': str(m.identifier),
                'number': int(m.number),
                'machine_type_display': m.get_machine_type_display(),
                'machine_status': m.machine_status,
                'remaining_time': m.remaining_time(),
                'end_time': timezone.localtime(m.end_time()).strftime('%a, %d %b %H:%M'),
                'notes': m.get_notes(),
                'notes_date': timezone.localtime(m.notes_date).strftime('%d.%m.%Y %H:%M')
            })

        return JsonResponse({'machines': machines_data})

    else:
        # GET-Request: Seite mit Maschinenliste zurückgeben
        machines = Machine.objects.filter(building=building)

        # Update all machines
        for m in machines:
            if m.update():
                if m.machine_status == 'F':
                    send_machine_finished_notification(m)

        return render(
            request, 'timer/index.html',
            {
                'building_description': markdown.markdown(bleach.clean(building.description)),
                'machines': machines,
                'building': building.get_name(),
                'building_code': building.identifier,
                'year': datetime.now().year
            }
        )

def set_timer(request, building, machine_id):
    if request.method == 'POST':
        machine = Machine.objects.get(identifier=machine_id)

        if machine is None:
            return JsonResponse({'status': 'error', 'message': 'Invalid machine'}, status=400)

        try:
            timer_duration = int(request.POST.get('timerDuration', 90))
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid timer duration'}, status=400)

        if (machine.machine_status == 'A' or machine.machine_status == 'F') and 180 >= timer_duration >= 1:
            machine.start_timer(timer=timer_duration)
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Machine is not available'}, status=400)

    return render(request, 'timer/404.html', {'year': datetime.now().year}, status=404)

def available(request, building, machine_id):
    if request.method == 'POST':
        try:
            machine = Machine.objects.get(identifier=machine_id, building=building)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid machine or building'}, status=400)

        if machine.machine_status == 'F':
            machine.set_available()

            # trigger notification
            send_machine_available_notification(machine)

            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Machine is not finished'}, status=400)

    return render(request, 'timer/404.html', {'year': datetime.now().year}, status=404)

def get_notes(request, building, machine_id):
    if request.method == 'POST':
        try:
            machine = Machine.objects.get(identifier=machine_id, building=building)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid machine or building'}, status=400)

        return JsonResponse({'status': 'success', 'notes': machine.get_notes()})

    return render(request, 'timer/404.html', {'year': datetime.now().year}, status=404)

def set_defect(request, building, machine_id):
    if request.method == 'POST':
        try:
            machine = Machine.objects.get(identifier=machine_id, building=building)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid machine or building'}, status=400)

        notes = request.POST.get('notes', '')

        if len(notes) > 500:
            return JsonResponse({'status': 'error', 'message': 'Notes too long'}, status=400)

        machine.set_defect(notes=notes)

        return JsonResponse({'status': 'success'})

    return render(request, 'timer/404.html', {'year': datetime.now().year}, status=404)

def set_repair(request, building, machine_id):
    if request.method == 'POST':
        try:
            machine = Machine.objects.get(identifier=machine_id, building=building)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid machine or building'}, status=400)

        machine.set_available()

        # trigger notification
        send_machine_available_notification(machine)

        machine.set_notes()

        return JsonResponse({'status': 'success'})

    return render(request, 'timer/404.html', {'year': datetime.now().year}, status=404)

def set_blinking(request, building, machine_id):
    if request.method == 'POST':
        try:
            machine = Machine.objects.get(identifier=machine_id, building=building)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid machine or building'}, status=400)

        machine.set_blinking()
        return JsonResponse({'status': 'success'})

    return render(request, 'timer/404.html', {'year': datetime.now().year}, status=404)

def page_not_found(request, exception):
    return render(request, 'timer/404.html', {'year': datetime.now().year}, status=404)

def homepage(request):
    return render(request, 'timer/home.html', {'year': datetime.now().year})
