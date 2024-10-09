# Generated by Django 5.1.1 on 2024-10-09 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('identifier', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.PositiveIntegerField()),
                ('building', models.CharField(choices=[('aa', 'Unity Alpha [A side]'), ('ab', 'Unity Alpha [B side]')], max_length=2)),
                ('machine_type', models.CharField(choices=[('W', 'Washer'), ('D', 'Dryer')], max_length=1)),
                ('machine_status', models.CharField(choices=[('A', 'Available'), ('R', 'Running'), ('F', 'Finished'), ('D', 'Defect')], default='A', max_length=1)),
                ('timer', models.PositiveIntegerField(default=90)),
                ('timer_start', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('notes_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
