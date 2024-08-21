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
    
