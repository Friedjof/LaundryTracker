import asyncio

import django.db.utils
from background_task import background
from telegram import Bot

from .models import TelegramChannel
from timer.models import Machine, Building


MESSAGES = {
    'available': '✅ Machine {machine_number} ({machine_type}) in building "{building_name}" is now available!',
    'finished': '🏁 Machine {machine_number} ({machine_type}) in building "{building_name}" has finished!',
}


async def send_update_notification(bot_token, chat_id, message):
    await Bot(token=bot_token).send_message(chat_id=chat_id, text=message)


def send_machine_available_notification(building: Building, machine: Machine):
    for channel in TelegramChannel.objects.filter(building=building):
        asyncio.run(send_update_notification(
            channel.telegram_bot.token, channel.chat_id, MESSAGES['available'].format(
                machine_number=machine.number, building_name=building.name, machine_type=machine.get_machine_type_display()
            )
        ))


def send_machine_finished_notification(building: Building, machine: Machine):
    for channel in TelegramChannel.objects.filter(building=building):
        asyncio.run(send_update_notification(
            channel.telegram_bot.token, channel.chat_id, MESSAGES['finished'].format(
                machine_number=machine.number, building_name=building.name, machine_type=machine.get_machine_type_display()
            )
        ))


@background(schedule=5)
def update_machine_status():
    machines = Machine.objects.filter(machine_status='R')
    for machine in machines:
        if machine.update(): # if machine was updated
            # trigger notification
            send_machine_finished_notification(machine.building, machine)


# hint from https://github.com/django-background-tasks/django-background-tasks/issues/205
try:
    update_machine_status(repeat=5, repeat_until=None)
except django.db.utils.OperationalError:
    print('Database not ready yet')
