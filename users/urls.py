"""
------------------------------------------------------------
 File        : users/urls.py
 Author      : Nandan A M
 Description : URL routing configuration for user management app.
               Defines all user-related endpoints including authentication,
               dashboard, QR code management, and activity logging.
 Created On  : 12-Dec-2025
 Version     : 1.0
------------------------------------------------------------
"""

from django.urls import path
from . import views

# URL patterns for user management and authentication
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generate-qr/', views.generate_qr, name='generate_qr'),
    path('revoke-qr/', views.revoke_qr, name='revoke_qr'),
    path('activate-qr/', views.activate_qr, name='activate_qr'),
    path('qr-login/', views.qr_login_page, name='qr_login_page'),
    path('api/qr-login/', views.qr_login, name='qr_login'),
    path('activity-logs/', views.activity_logs, name='activity_logs'),
    path('reports/', views.reports, name='reports'),
    path('export-report/', views.export_report, name='export_report'),
    path('api/dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
    path('logout/', views.user_logout, name='logout'),
    path('features/', views.features, name='features'),
    path('documentation/', views.documentation, name='documentation'),
    path('support/', views.support, name='support'),
]

