"""
------------------------------------------------------------
 File        : users/views.py
 Author      : Nandan A M
 Description : User authentication and management views for the
               AI-enhanced system call optimization application.
               Handles registration, login, QR code authentication,
               dashboard, activity logs, and reporting features.
 Created On  : 12-Dec-2025
 Version     : 1.0
------------------------------------------------------------
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import CustomUser, QRCode, ActivityLog, SystemHealth
from .forms import UserRegistrationForm, QRLoginForm
import json
from datetime import datetime, timedelta
from io import BytesIO
from django.core.files import File
import qrcode


def home(request):
    """Home page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'users/home.html')


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create QR code for the user
            QRCode.objects.create(user=user)
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Log activity
            ActivityLog.objects.create(
                user=user,
                action='login',
                description=f'User {user.username} logged in',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
def dashboard(request):
    """User dashboard"""
    user = request.user
    qr_code = None
    
    try:
        qr_code = user.qr_code
    except QRCode.DoesNotExist:
        # Create QR code if it doesn't exist
        qr_code = QRCode.objects.create(user=user)
    
    context = {
        'user': user,
        'qr_code': qr_code,
    }
    
    return render(request, 'users/dashboard.html', context)


@login_required
def generate_qr(request):
    """Generate or regenerate QR code"""
    user = request.user
    
    try:
        qr_code = user.qr_code
        # Force a brand new token for regeneration
        qr_code.token = ''
        qr_code.generate_token()
        qr_code.generate_qr_image()
        qr_code.activate()
        qr_code.save()
        messages.success(request, 'QR code regenerated successfully!')
        ActivityLog.objects.create(
            user=user,
            action='qr_generated',
            description='QR code regenerated',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    except QRCode.DoesNotExist:
        qr_code = QRCode.objects.create(user=user)
        messages.success(request, 'QR code generated successfully!')
        ActivityLog.objects.create(
            user=user,
            action='qr_generated',
            description='QR code generated',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    
    return redirect('dashboard')


@login_required
def revoke_qr(request):
    """Revoke QR code"""
    user = request.user
    
    try:
        qr_code = user.qr_code
        qr_code.revoke()
        messages.success(request, 'QR code revoked successfully!')
        ActivityLog.objects.create(
            user=user,
            action='qr_revoked',
            description='QR code revoked',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    except QRCode.DoesNotExist:
        messages.error(request, 'No QR code found.')
    
    return redirect('dashboard')


@login_required
def activate_qr(request):
    """Activate QR code"""
    user = request.user
    
    try:
        qr_code = user.qr_code
        qr_code.activate()
        messages.success(request, 'QR code activated successfully!')
    except QRCode.DoesNotExist:
        messages.error(request, 'No QR code found.')
    
    return redirect('dashboard')


@csrf_exempt
@require_http_methods(["POST"])
def qr_login(request):
    """QR code login endpoint - supports username|token and legacy token-only data"""
    try:
        data = json.loads(request.body)
        qr_data = data.get('qr_data') or data.get('token')
        print(f"[qr_login] payload={data}")

        if not qr_data:
            print("[qr_login] missing qr_data")
            return JsonResponse({'success': False, 'error': 'QR data is required'}, status=400)

        qr_data = qr_data.strip()

        # Preferred format: username|token for immediate login
        qr_code = None
        if '|' in qr_data:
            try:
                username, token = [p.strip() for p in qr_data.split('|', 1)]
                user = CustomUser.objects.get(username=username)
                qr_code = QRCode.objects.get(user=user, token=token, is_active=True)
            except (CustomUser.DoesNotExist, QRCode.DoesNotExist):
                print(f"[qr_login] invalid username|token: {qr_data}")
                return JsonResponse({'success': False, 'error': 'Invalid QR code data'}, status=404)
        else:
            # Legacy: token only
            try:
                qr_code = QRCode.objects.get(token=qr_data, is_active=True)
            except QRCode.DoesNotExist:
                print(f"[qr_login] token not found: {qr_data}")
                return JsonResponse({'success': False, 'error': 'Invalid QR code token. Please check your QR code.'}, status=404)
            except QRCode.MultipleObjectsReturned:
                print(f"[qr_login] multiple tokens found: {qr_data}")
                return JsonResponse({'success': False, 'error': 'Multiple QR codes found'}, status=500)

        if qr_code.revoked_at:
            print(f"[qr_login] token revoked: {qr_code.token}")
            return JsonResponse({'success': False, 'error': 'QR code has been revoked'}, status=403)

        qr_code.mark_as_used()
        
        # Log the user in and ensure session is saved
        login(request, qr_code.user, backend='django.contrib.auth.backends.ModelBackend')
        
        # Force session save to ensure cookie is set
        request.session.save()
        
        print(f"[qr_login] success username={qr_code.user.username}, session_key={request.session.session_key}")

        ActivityLog.objects.create(
            user=qr_code.user,
            action='qr_login',
            description=f'User {qr_code.user.username} logged in via QR code',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        return JsonResponse({
            'success': True,
            'message': 'Login successful',
            'user': {
                'username': qr_code.user.username,
                'email': qr_code.user.email,
                'role': qr_code.user.role,
            },
            'redirect_url': '/dashboard/'
        })

    except json.JSONDecodeError:
        print("[qr_login] invalid JSON")
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        import traceback
        print(f"QR Login Error: {e}")
        print(traceback.format_exc())
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'}, status=500)


def qr_login_page(request):
    """QR code login page"""
    return render(request, 'users/qr_login.html')


@login_required
def user_logout(request):
    """Custom logout view that redirects to login"""
    # Log activity before logout
    ActivityLog.objects.create(
        user=request.user,
        action='logout',
        description=f'User {request.user.username} logged out',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')


def features(request):
    """Features page"""
    return render(request, 'users/features.html')


def documentation(request):
    """Documentation page"""
    return render(request, 'users/documentation.html')


def support(request):
    """Support page"""
    return render(request, 'users/support.html')


def documentation(request):
    """Documentation page"""
    return render(request, 'users/documentation.html')


def support(request):
    """Support page"""
    return render(request, 'users/support.html')


@login_required
def activity_logs(request):
    """Activity logs page"""
    logs = ActivityLog.objects.filter(user=request.user).order_by('-created_at')
    
    # Filter by date range if provided
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    action_filter = request.GET.get('action')
    
    if date_from:
        logs = logs.filter(created_at__gte=date_from)
    if date_to:
        logs = logs.filter(created_at__lte=date_to)
    if action_filter:
        logs = logs.filter(action=action_filter)
    
    paginator = Paginator(logs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'actions': ActivityLog.ACTION_CHOICES,
    }
    return render(request, 'users/activity_logs.html', context)


@login_required
def reports(request):
    """Reports page"""
    # Get statistics
    total_logs = ActivityLog.objects.filter(user=request.user).count()
    recent_logs = ActivityLog.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    # Get activity by type
    activity_by_type = ActivityLog.objects.filter(user=request.user).values('action').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Get activity by date (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_activity = ActivityLog.objects.filter(
        user=request.user,
        created_at__gte=seven_days_ago
    ).extra(
        select={'day': "date(created_at)"}
    ).values('day').annotate(count=Count('id')).order_by('day')
    
    context = {
        'total_logs': total_logs,
        'recent_logs': recent_logs,
        'activity_by_type': activity_by_type,
        'recent_activity': recent_activity,
    }
    return render(request, 'users/reports.html', context)


@login_required
def export_report(request):
    """Export report as CSV"""
    import csv
    
    logs = ActivityLog.objects.filter(user=request.user).order_by('-created_at')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="activity_report_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Action', 'Description', 'IP Address'])
    
    for log in logs:
        writer.writerow([
            log.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            log.get_action_display(),
            log.description,
            log.ip_address or ''
        ])
    
    # Log the export
    ActivityLog.objects.create(
        user=request.user,
        action='report_generated',
        description='User exported activity report',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    return response


@login_required
def dashboard_stats(request):
    """Get dashboard statistics as JSON"""
    user = request.user
    
    # Get activity counts
    total_activities = ActivityLog.objects.filter(user=user).count()
    optimizations = ActivityLog.objects.filter(user=user, action='optimization').count()
    alerts = SystemHealth.objects.order_by('-created_at').first()
    alerts_count = alerts.critical_alerts if alerts else 0
    
    # Calculate performance score (mock for now)
    performance_score = min(100, max(0, 100 - (alerts_count * 10)))
    
    # Get recent activities
    recent_activities = ActivityLog.objects.filter(user=user).order_by('-created_at')[:5]
    activities_data = [{
        'action': log.get_action_display(),
        'description': log.description,
        'created_at': log.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    } for log in recent_activities]
    
    # Get performance trends (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    trends = []
    for i in range(7):
        date = timezone.now() - timedelta(days=6-i)
        count = ActivityLog.objects.filter(
            user=user,
            created_at__date=date.date()
        ).count()
        trends.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })
    
    return JsonResponse({
        'total_activities': total_activities,
        'optimizations': optimizations,
        'alerts': alerts_count,
        'performance_score': performance_score,
        'recent_activities': activities_data,
        'trends': trends,
    })

