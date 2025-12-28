"""
------------------------------------------------------------
 File        : syscall_optimizer/asgi.py
 Author      : Nandan A M
 Description : ASGI configuration for syscall_optimizer project.
               Exposes the ASGI callable as a module-level variable
               named 'application' for deployment on ASGI servers.
 Created On  : 12-Dec-2025
 Version     : 1.0
------------------------------------------------------------
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'syscall_optimizer.settings')

application = get_asgi_application()

