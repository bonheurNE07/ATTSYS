from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import StudentForm, EmployeeForm, RFIDCardForm
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

# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('core:login')

# Student Management Views (Create, Update and Delete)
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:student_list')
    else:
        form = StudentForm()

    return render(request, 'core/create_student.html', {'form': form})

# Student Management Update view
@login_required
def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('core:student_list')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'core/update_student.html', {'form': form})

# Student Management Delete view
@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('core:student_list')
    
    return render(request, 'core/delete_student.html', {'student': student})
         
# Employee Management views (Create, Upate, Delete)

# Employee Management Create View
@login_required
def create_employee(request):
    if request.methode == 'POST':
       form = EmployeeForm(request.POST, request.FILES)
       if form.is_valid():
           form.save()
           return redirect('core:employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'core/create_employee.html', {'form': form})
 
# Employee Management Update View
@login_required
def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('core:employee_list')
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'core/update_employee.html', {'form': form})

# Employee Management Delete View
@login_required
def delet_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('core:employee_list')
    
    return render(request, 'core/delete_employee.html', {'employee': employee})

# RFID Card Management Views (Assign, Update, Delete)

# RFID Card Management Assign View
@login_required
def assign_rfid(request):
    if request.method == 'POST':
        form = RFIDCardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "RFID Card assigned successfully!")
            return redirect('core:assign_rfid')
        else:
            form = RFIDCard()
        return render(request, 'core/assign_rfid.html', {'form': form})

# RFID Card Management Update view
@login_required
def update_rfid(request, pk):
    rfid_card = get_object_or_404(RFIDCard, pk=pk)
    if request.method == 'POST':
        form = RFIDCardForm(request.POST, instance=rfid_card)
        if form.is_valid():
            form.save()
            messages.success(request, "RFID Card updated successfully!")
            return redirect('core:update_rfid', pk=pk)
    else:
        form = RFIDCardForm(instance=rfid_card)

    return render(request, 'core/update_rfid.html', {'form': form, 'rfid_card': rfid_card})

# RFID Card Management Delete View
@login_required
def delete_rfid(request, pk):
    rfid_card = get_object_or_404(RFIDCard, pk=pk)
    if request.method == 'POST':
        rfid_card.delete()
        messages.success(request, "RFID Card deleted successfully!")
        
        return redirect('core:rfid_list') 
    return render(request, 'core/delete_rfid.html', {'rfid_card': rfid_card})