"""
------------------------------------------------------------
 File        : users/forms.py
 Author      : Nandan A M
 Description : Django forms for user registration and QR code login.
               Handles form validation, styling, and user creation
               with role-based access control.
 Created On  : 12-Dec-2025
 Version     : 1.0
------------------------------------------------------------
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    """User registration form"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        initial='user',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class to all fields for proper Bootstrap styling
        for field_name, field in self.fields.items():
            if field_name == 'role':
                continue
            # Check if widget has attrs, if not create it
            if not hasattr(field.widget, 'attrs'):
                field.widget.attrs = {}
            elif field.widget.attrs is None:
                field.widget.attrs = {}
            # Update attrs to include form-control class
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
        
        # Hide role field for regular users (only admins can set roles during registration)
        # Regular users will always get 'user' role
        if not kwargs.get('initial', {}).get('is_staff'):
            self.fields['role'].widget = forms.HiddenInput()
            self.fields['role'].initial = 'user'
        else:
            # If role is visible, ensure it has form-control class
            if not hasattr(self.fields['role'].widget, 'attrs'):
                self.fields['role'].widget.attrs = {}
            elif self.fields['role'].widget.attrs is None:
                self.fields['role'].widget.attrs = {}
            self.fields['role'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.role = self.cleaned_data.get('role', 'user')
        
        if commit:
            user.save()
        return user


class QRLoginForm(forms.Form):
    """QR code login form"""
    token = forms.CharField(max_length=64, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

