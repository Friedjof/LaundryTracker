# Generated by Django 5.1.1 on 2024-10-15 13:54

from django.db import migrations, models


def set_default_name(apps, schema_editor):
    Machine = apps.get_model('timer', 'Machine')
    for machine in Machine.objects.all():
        machine.name = str(machine.number)
        machine.save()


class Migration(migrations.Migration):

    dependencies = [
        ('timer', '0009_building_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='name',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AlterField(
            model_name='machine',
            name='machine_type',
            field=models.CharField(choices=[('W', 'Washer'), ('D', 'Dryer')], default='W', max_length=1),
        ),
        migrations.RunPython(set_default_name),
    ]
