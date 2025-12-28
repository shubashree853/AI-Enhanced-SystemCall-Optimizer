"""
------------------------------------------------------------
 File        : users/models.py
 Author      : Nandan A M
 Description : Database models for user management, QR code
               authentication, activity logging, and system health
               monitoring in the AI-enhanced system call optimizer.
 Created On  : 12-Dec-2025
 Version     : 1.0
------------------------------------------------------------
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image


class CustomUser(AbstractUser):
    """Custom user model with role-based access"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('user', 'User'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser
    
    def is_staff_user(self):
        return self.role == 'staff' or self.is_staff
    
    def is_regular_user(self):
        return self.role == 'user'


class QRCode(models.Model):
    """QR Code model for user authentication"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='qr_code')
    token = models.CharField(max_length=64, unique=True, editable=False)
    qr_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'QR Code'
        verbose_name_plural = 'QR Codes'
    
    def __str__(self):
        return f"QR Code for {self.user.username}"
    
    def generate_token(self):
        """Generate a unique token for the QR code"""
        if not self.token:
            self.token = secrets.token_urlsafe(32)
        return self.token
    
    def generate_qr_image(self):
        """Generate QR code image containing username|token for quick login"""
        if not self.token:
            self.generate_token()

        # Encode username and token so the scanner can log in instantly
        qr_data = f"{self.user.username}|{self.token}"
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Save to model
        self.qr_image.save(
            f'qr_{self.user.username}_{self.token[:8]}.png',
            File(buffer),
            save=False
        )
    
    def revoke(self):
        """Revoke the QR code"""
        self.is_active = False
        self.revoked_at = timezone.now()
        self.save()
    
    def activate(self):
        """Activate the QR code"""
        self.is_active = True
        self.revoked_at = None
        self.save()
    
    def mark_as_used(self):
        """Mark QR code as used"""
        self.last_used = timezone.now()
        self.save()
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.generate_token()
        if not self.qr_image:
            self.generate_qr_image()
        super().save(*args, **kwargs)


class ActivityLog(models.Model):
    """Activity log for user actions"""
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('qr_login', 'QR Code Login'),
        ('qr_generated', 'QR Code Generated'),
        ('qr_revoked', 'QR Code Revoked'),
        ('optimization', 'Optimization Performed'),
        ('report_generated', 'Report Generated'),
        ('settings_changed', 'Settings Changed'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.created_at}"


class SystemHealth(models.Model):
    """System health monitoring"""
    cpu_usage = models.FloatField(default=0.0)
    memory_usage = models.FloatField(default=0.0)
    disk_usage = models.FloatField(default=0.0)
    active_users = models.IntegerField(default=0)
    total_syscalls = models.IntegerField(default=0)
    critical_alerts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'System Health'
        verbose_name_plural = 'System Health Records'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"System Health - {self.created_at}"