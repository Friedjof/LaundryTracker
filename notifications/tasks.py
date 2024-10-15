import asyncio

import django.db.utils
import telegram

from .models import TelegramChannel
from timer.models import Machine, Building


MESSAGES = {
    'available': '✅ Machine {machine_number} ({machine_type}) in building "{building_name}" is now available!',
    'finished': '🏁 Machine {machine_number} ({machine_type}) in building "{building_name}" has finished!',
}


async def send_update_notification(bot_token, chat_id, message):
    try:
        await telegram.Bot(token=bot_token).send_message(chat_id=chat_id, text=message)
    except telegram.error.BadRequest as e:
        print(f'Error sending message: {e}')


def send_machine_available_notification(machine: Machine):
    for channel in TelegramChannel.objects.filter(building=machine.building):
        asyncio.run(send_update_notification(
            channel.telegram_bot.token, channel.chat_id, MESSAGES['available'].format(
                machine_number=machine.name, building_name=machine.building.name, machine_type=machine.get_machine_type_display()
            )
        ))


def send_machine_finished_notification(machine: Machine):
    for channel in TelegramChannel.objects.filter(building=machine.building):
        asyncio.run(send_update_notification(
            channel.telegram_bot.token, channel.chat_id, MESSAGES['finished'].format(
                machine_number=machine.name, building_name=machine.building.name, machine_type=machine.get_machine_type_display()
            )
        ))
