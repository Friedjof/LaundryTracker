import markdown
import bleach

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render

from .models import Machine, Building

from notifications.tasks import send_machine_available_notification, send_machine_finished_notification


def index(request, building):
    try:
        building = Building.objects.get(identifier=building)
    except ObjectDoesNotExist:
        return render(request, 'timer/404.html', status=404)

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
                'name': m.name,
                'type': m.get_type(),
                'status': m.get_status(),
                'time': m.get_time_note(),
                'notes': m.get_notes()
            })

        return JsonResponse({'machines': machines_data})

    else:
        # GET-Request: Seite mit Maschinenliste zurückgeben
        machines = []

        # Update all machines
        for m in Machine.objects.filter(building=building):
            if m.update():
                if m.machine_status == 'F':
                    send_machine_finished_notification(m)

            machines.append({
                'identifier': str(m.identifier),
                'number': int(m.number),
                'name': m.name,
                'type': m.get_type(),
                'status': m.get_status(),
                'time': m.get_time_note(),
                'notes': m.get_notes()
            })

        return render(
            request, 'timer/index.html',
            {
                'title': building.get_name(),
                'building': building.get_name(),
                'building_identifier': building.identifier,
                'building_description': markdown.markdown(bleach.clean(building.description)),
                'machines': machines
            }
        )

def set_timer(request, building, machine_id):
    if request.method == 'POST':
        machine = Machine.objects.get(identifier=machine_id, building=building)

        if machine is None:
            return JsonResponse({'status': 'error', 'message': 'Invalid machine'}, status=400)

        try:
            timer_duration = int(request.POST.get('timerDuration', 90))
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid timer duration'}, status=400)

        try:
            will_ask_for = request.POST.get('will_ask_for_data_donation', 'true').lower() == 'true'
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid ask_for'}, status=400)

        if (machine.machine_status == 'A' or machine.machine_status == 'F') and 180 >= timer_duration >= 1:
            machine.start_timer(timer=timer_duration)

            machine_ask_for = Machine.get_longest_unused_machine(building)

            # returns machine is not updated since 12 hours
            if machine_ask_for is not None and machine_ask_for.elapsed_time() > 6 * 60:
                return JsonResponse({'status': 'success', 'ask_for': machine_ask_for.as_dict() if will_ask_for else None})

            return JsonResponse({'status': 'success', 'ask_for': None})
        return JsonResponse({'status': 'error', 'message': 'Machine is not available'}, status=400)

    return render(request, 'timer/404.html', status=404)

def set_available(request, building, machine_id):
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

    return render(request, 'timer/404.html', status=404)

def get_notes(request, building, machine_id):
    if request.method == 'POST':
        try:
            machine = Machine.objects.get(identifier=machine_id, building=building)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid machine or building'}, status=400)

        return JsonResponse({'status': 'success', 'notes': machine.get_notes()})

    return render(request, 'timer/404.html', status=404)

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

    return render(request, 'timer/404.html', status=404)

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

    return render(request, 'timer/404.html', status=404)

def set_blinking(request, building, machine_id):
    if request.method == 'POST':
        try:
            machine = Machine.objects.get(identifier=machine_id, building=building)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid machine or building'}, status=400)

        machine.set_blinking()
        return JsonResponse({'status': 'success'})

    return render(request, 'timer/404.html', status=404)

def set_finished(request, building, machine_id):
    if request.method == 'POST':
        try:
            machine = Machine.objects.get(identifier=machine_id, building=building)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid machine or building'}, status=400)

        machine.set_finished()
        return JsonResponse({'status': 'success'})

    return render(request, 'timer/404.html', status=404)

def set_unchanged(request, building, machine_id):
    if request.method == 'POST':
        try:
            machine = Machine.objects.get(identifier=machine_id, building=building)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid machine or building'}, status=400)

        machine.set_unchanged()
        return JsonResponse({'status': 'success'})

    return render(request, 'timer/404.html', status=404)

def page_not_found(request, exception):
    return render(request, 'timer/404.html', status=404)

def homepage(request):
    return render(request, 'timer/home.html')
