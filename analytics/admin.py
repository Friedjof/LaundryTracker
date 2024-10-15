import io
import base64

from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.db import models
from django.db.models import OuterRef, Subquery

import matplotlib.pyplot as plt

from timer.models import Building
from .models import History
from .tasks import Diagrams


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'created_at', 'building_identifier', 'building', 'machine_identifier', 'machine_type', 'machine_status', 'machine_number', 'timer', 'timer_start', 'notes', 'notes_date')
    list_filter = ('building', 'machine_type', 'machine_status')
    search_fields = ('machine_identifier',)
    date_hierarchy = 'created_at'
    readonly_fields = ('identifier', 'created_at', 'building', 'machine_identifier', 'machine_type', 'machine_status', 'machine_number', 'timer', 'timer_start', 'notes', 'notes_date')
    fieldsets = (
        ('General', {
            'fields': ('created_at', 'identifier', 'building')
        }),
        ('Machine', {
            'fields': ('machine_identifier', 'machine_type', 'machine_status', 'machine_number', 'timer', 'timer_start')
        }),
        ('Notes', {
            'fields': ('notes', 'notes_date')
        }),
    )
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('analytics/', self.admin_site.admin_view(self.analytics_view), name='analytics')
        ]
        return custom_urls + urls

    @staticmethod
    def analytics_view(request):
        try:
            charts = [
                # first row
                Diagrams.map_weekday_hour_diagram(),
                Diagrams.running_machines_per_weekday_avg_linechart(),
                Diagrams.last_3_weeks_of_running_machines(),
                # second row
                Diagrams.last_3_weeks_of_machine_status(),
                Diagrams.avg_running_time_per_machine_type(),
                Diagrams.used_machines_per_type_and_building(),
                # third row
                Diagrams.machine_status_distribution(),
                Diagrams.states_per_building(),
                Diagrams.machine_types_per_building(),
            ]
        except Exception as e:
            print(e)
            charts = []

        return render(request, 'admin/analytics.html', context={'charts': charts})
