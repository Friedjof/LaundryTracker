# Generated by Django 5.1.1 on 2024-10-14 21:20

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('building_identifier', models.UUIDField(editable=False)),
                ('building', models.CharField(editable=False, max_length=100)),
                ('machine_identifier', models.UUIDField(editable=False)),
                ('machine_type', models.CharField(choices=[('W', 'Washer'), ('D', 'Dryer')], editable=False, max_length=100)),
                ('machine_status', models.CharField(choices=[('A', 'Available'), ('R', 'Running'), ('F', 'Finished'), ('D', 'Defect'), ('B', 'Blinking'), ('U', 'Unknown')], editable=False, max_length=100)),
                ('timer', models.IntegerField(editable=False)),
                ('timer_start', models.DateTimeField(editable=False)),
                ('notes', models.TextField(editable=False)),
                ('notes_date', models.DateTimeField(editable=False)),
            ],
        ),
    ]