"""
------------------------------------------------------------
 File        : optimizer/apps.py
 Author      : Nandan A M
 Description : Django app configuration for the optimizer application.
               Defines app metadata and default auto field settings.
 Created On  : 12-Dec-2025
 Version     : 1.0
------------------------------------------------------------
"""

from django.apps import AppConfig


class OptimizerConfig(AppConfig):
    """Configuration class for the optimizer Django app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'optimizer'

