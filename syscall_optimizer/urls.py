"""
------------------------------------------------------------
 File        : syscall_optimizer/urls.py
 Author      : Nandan A M
 Description : Root URL configuration for the Django project.
               Includes admin panel, user app, and optimizer app URLs.
               Handles static and media file serving in development.
 Created On  : 12-Dec-2025
 Version     : 1.0
------------------------------------------------------------
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

# Root URL patterns - includes all app URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('optimizer/', include('optimizer.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

