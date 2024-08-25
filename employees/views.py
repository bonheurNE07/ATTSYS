from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Employee
from .forms import EmployeeForm

# Utility function to check if the user is HOD (for access control)
def is_hod(user):
    return user.user_type == 1

@login_required
@user_passes_test(is_hod)
def employee_list(request):
    employees = Employee.objects.all()
    context = {
        'employees': employees,
    }
    return render(request, 'employee/employee_list.html', context)

@login_required
@user_passes_test(is_hod)
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully.')
            return redirect('employee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm()
    
    context = {
        'form': form,
    }
    return render(request, 'employee/add_employee.html', context)

@login_required
@user_passes_test(is_hod)
def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm(instance=employee)
    
    context = {
        'form': form,
        'employee': employee,
    }
    return render(request, 'employee/update_employee.html', context)

@login_required
@user_passes_test(is_hod)
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully.')
        return redirect('employee_list')
    
    context = {
        'employee': employee,
    }
    return render(request, 'employee/delete_employee.html', context)
