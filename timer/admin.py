from django.contrib import admin
from django.conf import settings
from django.utils import timezone
from django.utils.html import format_html
from django.contrib.auth.models import Group
from django.apps import AppConfig
from django.db.models.signals import post_migrate

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Machine, Building, BuildingAssignment


def create_moderator_group(sender, **kwargs):
    Group.objects.get_or_create(name='Moderator')


class TimerConfig(AppConfig):
    name = 'timer'

    def ready(self):
        post_migrate.connect(create_moderator_group, sender=self)


class BuildingResource(resources.ModelResource):
    class Meta:
        model = Building
        fields = ('identifier', 'name')
        import_id_fields = ('identifier',)
        export_order = ('identifier', 'name')


@admin.register(Building)
class BuildingAdmin(ImportExportModelAdmin):
    resource_class = BuildingResource
    list_display = ('identifier', 'name', 'building_link', 'machine_count')

    def building_link(self, obj):
        protocol = 'https' if settings.TLS_ACTIVE else 'http'
        domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'
        url = f"{protocol}://{domain}/{obj.identifier}"
        return format_html('<a href="{}" target="_blank">{}</a>', url, url)

    def get_queryset(self, request):
        # Superuser haben Zugriff auf alle Gebäude
        if request.user.is_superuser:
            return super().get_queryset(request)

        if request.user.groups.filter(name='Moderator').exists():
            return Building.objects.filter(buildingassignment__user=request.user)

        return Building.objects.none()

    def machine_count(self, obj):
        return obj.machine_set.count()

    machine_count.short_description = 'Number of Machines'

    building_link.short_description = 'Building Link'

class BuildingFilter(admin.SimpleListFilter):
    title = 'Building'
    parameter_name = 'building'

    def lookups(self, request, model_admin):
        # Superuser sehen alle Gebäude
        if request.user.is_superuser:
            buildings = Building.objects.all()
        else:
            # Moderatoren sehen nur die ihnen zugewiesenen Gebäude
            buildings = [a.building.identifier for a in BuildingAssignment.objects.filter(user=request.user)]
            buildings = Building.objects.filter(pk__in=buildings)

        # Erstelle eine Liste der Gebäude, die im Filter angezeigt werden sollen
        return [(building.identifier, building.name) for building in buildings]

    def queryset(self, request, queryset):
        # Filtere die Räume basierend auf dem ausgewählten Gebäude
        if self.value():
            return queryset.filter(building_id=self.value())
        return queryset

class MachineResource(resources.ModelResource):
    class Meta:
        model = Machine
        fields = ('identifier', 'number', 'building', 'machine_type', 'machine_status', 'timer', 'timer_start', 'notes', 'notes_date')
        import_id_fields = ('identifier',)
        export_order = ('identifier', 'number', 'building', 'machine_type', 'machine_status', 'timer', 'timer_start', 'notes', 'notes_date')


from datetime import timedelta

@admin.register(Machine)
class MachineAdmin(ImportExportModelAdmin):
    resource_class = MachineResource
    list_display = ('number', 'building_link', 'machine_type', 'machine_status', 'timer_minutes', 'timer_start', 'remaining_time', 'notes', 'notes_date')
    list_filter = (BuildingFilter, 'machine_type', 'machine_status')
    search_fields = ('number', 'building__name', 'machine_type')
    ordering = ('number',)
    readonly_fields = ('timer_start',)
    fieldsets = (
        (None, {
            'fields': ('number', 'building', 'machine_type', 'machine_status')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('timer', 'timer_start', 'notes', 'notes_date'),
        }),
    )

    def building_link(self, obj):
        protocol = 'https' if settings.TLS_ACTIVE else 'http'
        domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'
        url = f"{protocol}://{domain}/{obj.building.identifier}"
        return format_html('<a href="{}" target="_blank">{}</a>', url, obj.building.name)

    building_link.short_description = 'Building'

    def timer_minutes(self, obj):
        if obj.timer is None:
            return 'None'
        elif obj.timer == 1:
            return f"{obj.timer} minute"
        else:
            return f"{obj.timer} minutes"

    timer_minutes.short_description = 'Timer (minutes)'

    def remaining_time(self, obj):
        if obj.timer_start and obj.timer:
            end_time = obj.timer_start + timedelta(minutes=obj.timer)
            remaining = end_time - timezone.now()

            if remaining.total_seconds() > 0:
                return str(remaining).split('.')[0]

            if obj.machine_status == 'R':
                return 'Expired (not updated)'

            return 'Expired'
        return 'Undefined' if obj.timer != 0 else 'Expired'

    remaining_time.short_description = 'Remaining Time'

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        if request.user.groups.filter(name='Moderator').exists():
            return Machine.objects.filter(building__buildingassignment__user=request.user)

        return Machine.objects.none()


class BuildingAssignmentResource(resources.ModelResource):
    class Meta:
        model = BuildingAssignment
        fields = ('user', 'building')
        import_id_fields = ('user', 'building')
        export_order = ('user', 'building')


@admin.register(BuildingAssignment)
class BuildingAssignmentAdmin(ImportExportModelAdmin):
    resource_class = BuildingAssignmentResource
    list_display = ('user', 'building_link')
    list_filter = ('building',)
    search_fields = ('user__username', 'building__name')
    ordering = ('user', 'building')

    def building_link(self, obj):
        protocol = 'https' if settings.TLS_ACTIVE else 'http'
        domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'
        url = f"{protocol}://{domain}/{obj.building.identifier}"
        return format_html('<a href="{}" target="_blank">{}</a>', url, obj.building.name)

    building_link.short_description = 'Building'

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)

        if request.user.groups.filter(name='Moderator').exists():
            return BuildingAssignment.objects.filter(user=request.user)

        return BuildingAssignment.objects.none()