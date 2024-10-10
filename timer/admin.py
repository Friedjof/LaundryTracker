from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Machine, Building


class BuildingResource(resources.ModelResource):
    class Meta:
        model = Building
        fields = ('name',)


@admin.register(Building)
class BuildingAdmin(ImportExportModelAdmin):
    resource_class = BuildingResource
    list_display = ('identifier', 'name')


class MachineResource(resources.ModelResource):
    class Meta:
        model = Machine
        fields = ('number', 'building', 'machine_type', 'machine_status', 'timer', 'timer_start', 'notes', 'notes_date')


@admin.register(Machine)
class MachineAdmin(ImportExportModelAdmin):
    resource_class = MachineResource
    list_display = ('number', 'building', 'machine_type', 'machine_status', 'timer', 'timer_start', 'notes', 'notes_date')
