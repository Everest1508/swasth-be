from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import requests


def home(request):
    """Home page"""
    return render(request, 'home.html')


def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')


@login_required
def dashboard(request):
    """Dashboard based on user role"""
    user = request.user
    
    if user.role == 'admin':
        return render(request, 'admin_dashboard.html')
    elif user.role == 'doctor':
        return render(request, 'doctor_dashboard.html')
    elif user.role == 'pharmacy':
        return render(request, 'pharmacy_dashboard.html')
    else:
        return render(request, 'patient_dashboard.html')


def apply_doctor(request):
    """Doctor application page"""
    return render(request, 'apply_doctor.html')


def apply_pharmacy(request):
    """Pharmacy application page"""
    return render(request, 'apply_pharmacy.html')


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

