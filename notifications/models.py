import uuid

from django.db import models

from timer.models import Building


# Create your models here.
class TelegramBot(models.Model):
    identifier = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    name = models.CharField(max_length=100)
    token = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class TelegramChannel(models.Model):
    identifier = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    name = models.CharField(max_length=100)
    chat_id = models.BigIntegerField()

    telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
