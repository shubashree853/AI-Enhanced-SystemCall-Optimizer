"""
------------------------------------------------------------
 File        : syscall_optimizer/admin.py
 Author      : Nandan A M
 Description : Django admin site customization for the project.
               Sets custom headers, titles, and branding for the
               admin interface.
 Created On  : 12-Dec-2025
 Version     : 1.0
------------------------------------------------------------
"""

from django.contrib import admin

# Customize admin site with project branding
admin.site.site_header = "System Call Optimizer Administration"
admin.site.site_title = "System Call Optimizer Admin"
admin.site.index_title = "Welcome to System Call Optimizer Administration"

