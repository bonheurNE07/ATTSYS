from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import StudentForm, EmployeeForm
from .models import Student, Employee, User, RFIDCard

# Build the view for User registration (for HOD to create Employee accounts)
@login_required
def registration_employee(request):
    if request.user.user_type != 1: # To give only HODs the ability to register employees
        return redirect('core:home')

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee account created successfully!")
            return redirect('core:employee_list')
        else:
            form = EmployeeForm()
        
        return render(request, 'core/register_employee.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('core:home')
            else:
                messages.error(request, "Invaid username or password.")
        else:
            messages.error(request, "Invalid username or paswod.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})
