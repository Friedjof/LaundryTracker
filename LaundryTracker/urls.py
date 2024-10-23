"""
URL configuration for LaundryTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# this import is required to overwrite the default 404 handler
from timer.views import page_not_found

handler404 = page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('timer.urls')),
    path('laundry/', include('laundry.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
