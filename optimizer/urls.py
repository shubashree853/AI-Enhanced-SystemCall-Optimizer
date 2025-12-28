"""
------------------------------------------------------------
 File        : optimizer/urls.py
 Author      : Nandan A M
 Description : URL routing configuration for system call optimizer app.
               Defines endpoints for performance data, recommendations,
               categories, and syscall details.
 Created On  : 12-Dec-2025
 Version     : 1.0
------------------------------------------------------------
"""

from django.urls import path
from . import views

# URL patterns for optimizer functionality
urlpatterns = [
    path('', views.optimizer_dashboard, name='optimizer_dashboard'),
    path('performance/', views.performance_data, name='performance_data'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('categories/', views.categories, name='categories'),
    path('syscall/<str:syscall_name>/', views.syscall_details, name='syscall_details'),
    path('generate-fake-data/', views.generate_fake_data, name='generate_fake_data'),
]

