# Generated by Django 5.1.1 on 2024-10-14 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timer', '0008_alter_machine_machine_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]