import asyncio

import django.db.utils
from background_task import background
from telegram import Bot

from .models import TelegramChannel
from timer.models import Machine


async def send_update_notification(bot_token, chat_id, message):
    await Bot(token=bot_token).send_message(chat_id=chat_id, text=message)


@background(schedule=5)
def update_machine_status():
    machines = Machine.objects.filter(machine_status='R')
    for machine in machines:
        if machine.update():
            for channel in TelegramChannel.objects.filter(building=machine.building):
                asyncio.run(send_update_notification(channel.telegram_bot.token, channel.chat_id, f'Machine {machine.number} is finished'))


# hint from https://github.com/django-background-tasks/django-background-tasks/issues/205
try:
    update_machine_status(repeat=5, repeat_until=None)
except django.db.utils.OperationalError:
    print('Database not ready yet')
