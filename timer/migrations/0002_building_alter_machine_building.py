# Generated by Django 5.1.1 on 2024-10-09 11:14

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('identifier', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(code='invalid_short_name', message='Short name must contain only lowercase letters and periods.', regex='^[a-z.]+$')])),
            ],
        ),
        migrations.AlterField(
            model_name='machine',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timer.building'),
        ),
    ]
