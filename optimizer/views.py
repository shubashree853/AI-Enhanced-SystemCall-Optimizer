"""
------------------------------------------------------------
 File        : optimizer/views.py
 Author      : Nandan A M
 Description : View handlers for the system call optimizer dashboard
               and API endpoints. Provides performance data, recommendations,
               categories, and syscall details to authenticated users.
 Created On  : 12-Dec-2025
 Version     : 1.0
------------------------------------------------------------
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .optimizer import syscall_optimizer


def is_admin_or_staff(user):
    """Check if user is admin or staff"""
    return user.is_authenticated and (user.is_admin_user() or user.is_staff_user())


@login_required
def optimizer_dashboard(request):
    """System call optimizer dashboard"""
    refresh_interval = syscall_optimizer.get_refresh_interval()
    return render(request, 'optimizer/dashboard.html', {
        'refresh_interval': refresh_interval
    })


@login_required
def performance_data(request):
    """Get performance data as JSON"""
    data = syscall_optimizer.get_performance_data()
    return JsonResponse(data)


@login_required
def recommendations(request):
    """Get optimization recommendations as JSON"""
    data = syscall_optimizer.generate_optimization_strategy()
    return JsonResponse(data, safe=False)


@login_required
def categories(request):
    """Get syscall categories as JSON"""
    data = syscall_optimizer.get_syscall_categories()
    return JsonResponse(data)


@login_required
def syscall_details(request, syscall_name):
    """Get details for a specific syscall"""
    data = syscall_optimizer.get_syscall_details(syscall_name)
    return JsonResponse(data)


@login_required
def generate_fake_data(request):
    """Generate fake system call data for demonstration"""
    import random
    common_syscalls = [
        'read', 'write', 'open', 'close', 'mmap', 'munmap', 'mprotect',
        'futex', 'clock_gettime', 'select', 'poll', 'epoll_wait',
        'fork', 'clone', 'execve', 'wait4', 'exit',
        'stat', 'fstat', 'lstat', 'access', 'chmod',
        'socket', 'connect', 'accept', 'send', 'recv',
        'pipe', 'dup', 'dup2', 'fcntl', 'ioctl', 'brk', 'madvise'
    ]
    
    # Generate multiple syscalls
    for _ in range(30):
        syscall_name = random.choice(common_syscalls)
        execution_time = random.uniform(0.0001, 0.2)
        category = syscall_optimizer.get_category_for_syscall(syscall_name)
        syscall_optimizer.record_syscall_performance(syscall_name, execution_time, category)
    
    return JsonResponse({'success': True, 'message': 'Fake system call data generated successfully'})