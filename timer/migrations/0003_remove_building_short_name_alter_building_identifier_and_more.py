# Generated by Django 5.1.1 on 2024-10-09 11:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timer', '0002_building_alter_machine_building'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='short_name',
        ),
        migrations.AlterField(
            model_name='building',
            name='identifier',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='machine',
            name='timer',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
