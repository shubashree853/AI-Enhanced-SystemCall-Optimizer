"""
------------------------------------------------------------
 File        : users/admin.py
 Author      : Nandan A M
 Description : Django admin interface configuration for user management.
               Provides admin views for CustomUser and QRCode models with
               custom actions for role management and QR code operations.
 Created On  : 12-Dec-2025
 Version     : 1.0
------------------------------------------------------------
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import CustomUser, QRCode


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin interface for CustomUser"""
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined', 'has_qr_code']
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('role', 'phone_number',)
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('role', 'phone_number',)
        }),
    )
    
    actions = ['make_admin', 'make_staff', 'make_user']
    
    def has_qr_code(self, obj):
        return hasattr(obj, 'qr_code')
    has_qr_code.boolean = True
    has_qr_code.short_description = 'Has QR Code'
    
    def make_admin(self, request, queryset):
        queryset.update(role='admin')
    make_admin.short_description = "Mark selected users as Admin"
    
    def make_staff(self, request, queryset):
        queryset.update(role='staff')
    make_staff.short_description = "Mark selected users as Staff"
    
    def make_user(self, request, queryset):
        queryset.update(role='user')
    make_user.short_description = "Mark selected users as Regular User"


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    """Admin interface for QRCode"""
    list_display = ['user', 'token_preview', 'is_active', 'created_at', 'last_used', 'revoked_at']
    list_filter = ['is_active', 'created_at', 'revoked_at']
    search_fields = ['user__username', 'user__email', 'token']
    readonly_fields = ['token', 'created_at', 'last_used', 'revoked_at', 'qr_image_preview']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('QR Code Details', {
            'fields': ('token', 'qr_image', 'qr_image_preview', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_used', 'revoked_at')
        }),
    )
    
    actions = ['revoke_qr_codes', 'activate_qr_codes', 'regenerate_qr_codes']
    
    def token_preview(self, obj):
        return f"{obj.token[:16]}..." if obj.token else "No token"
    token_preview.short_description = 'Token'
    
    def qr_image_preview(self, obj):
        if obj.qr_image:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', obj.qr_image.url)
        return "No QR code image"
    qr_image_preview.short_description = 'QR Code Preview'
    
    def revoke_qr_codes(self, request, queryset):
        for qr in queryset:
            qr.revoke()
        self.message_user(request, f"{queryset.count()} QR code(s) revoked.")
    revoke_qr_codes.short_description = "Revoke selected QR codes"
    
    def activate_qr_codes(self, request, queryset):
        for qr in queryset:
            qr.activate()
        self.message_user(request, f"{queryset.count()} QR code(s) activated.")
    activate_qr_codes.short_description = "Activate selected QR codes"
    
    def regenerate_qr_codes(self, request, queryset):
        for qr in queryset:
            qr.generate_token()
            qr.generate_qr_image()
            qr.save()
        self.message_user(request, f"{queryset.count()} QR code(s) regenerated.")
    regenerate_qr_codes.short_description = "Regenerate selected QR codes"

