from django.urls import path, re_path

from .views import index
from .consumers import LaundryConsumer, EchoConsumer

urlpatterns = [
    path('', index, name='index'),
    re_path(r'ws/laundry/$', LaundryConsumer.as_asgi())
]