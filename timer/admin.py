from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Machine, Building


class BuildingResource(resources.ModelResource):
    class Meta:
        model = Building
        fields = ('identifier', 'name')
        import_id_fields = ('identifier',)
        export_order = ('identifier', 'name')


@admin.register(Building)
class BuildingAdmin(ImportExportModelAdmin):
    resource_class = BuildingResource
    list_display = ('identifier', 'name', 'building_link')

    def building_link(self, obj):
        protocol = 'https' if settings.TLS_ACTIVE else 'http'
        domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'
        url = f"{protocol}://{domain}/{obj.identifier}"
        return format_html('<a href="{}" target="_blank">{}</a>', url, url)

    building_link.short_description = 'Building Link'


class MachineResource(resources.ModelResource):
    class Meta:
        model = Machine
        fields = ('identifier', 'number', 'building', 'machine_type', 'machine_status', 'timer', 'timer_start', 'notes', 'notes_date')
        import_id_fields = ('identifier',)
        export_order = ('identifier', 'number', 'building', 'machine_type', 'machine_status', 'timer', 'timer_start', 'notes', 'notes_date')


@admin.register(Machine)
class MachineAdmin(ImportExportModelAdmin):
    resource_class = MachineResource
    list_display = ('number', 'building', 'machine_type', 'machine_status', 'timer', 'timer_start', 'notes', 'notes_date')
