"""
------------------------------------------------------------
 File        : syscall_optimizer/wsgi.py
 Author      : Nandan A M
 Description : WSGI configuration for syscall_optimizer project.
               Exposes the WSGI callable as a module-level variable
               named 'application' for deployment on WSGI servers.
 Created On  : 12-Dec-2025
 Version     : 1.0
------------------------------------------------------------
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'syscall_optimizer.settings')

application = get_wsgi_application()

