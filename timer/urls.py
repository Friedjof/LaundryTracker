import uuid

from django.urls import path, register_converter

from .views import index, set_timer, available, get_notes, set_defect, set_repair, page_not_found, homepage


class UUIDConverter:
    regex = r'[0-9a-f]{32}|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

    @staticmethod
    def to_python(value):
        return uuid.UUID(value)

    @staticmethod
    def to_url(value):
        return str(value)

register_converter(UUIDConverter, 'uuid')

handler404 = page_not_found

urlpatterns = [
    path('building/<uuid:building>/', index),
    path('building/<uuid:building>/laundry/<uuid:machine_id>/', set_timer, name='set_timer'),
    path('building/<uuid:building>/laundry/<uuid:machine_id>/available/', available, name='available'),
    path('building/<uuid:building>/laundry/<uuid:machine_id>/notes/', get_notes, name='get_notes'),
    path('building/<uuid:building>/laundry/<uuid:machine_id>/defect/', set_defect, name='set_defect'),
    path('building/<uuid:building>/laundry/<uuid:machine_id>/repair/', set_repair, name='set_repair'),
    path('404', lambda request: page_not_found(request, None), name='404'),
    path('', homepage, name='homepage'),
]