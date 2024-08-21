from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import StudentForm, EmployeeForm, RFIDCardForm
from .models import Student, Employee, User, RFIDCard 
from courses.models import Course
from exams.models import Exam
from attendance.models import AttendanceRecord

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
        
        return render(request, 'core/registration/register_employee.html', {'form': form})

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
    
    return render(request, 'core/registration/login.html', {'form': form})

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

    return render(request, 'core/student/create_student.html', {'form': form})

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
    
    return render(request, 'core/student/update_student.html', {'form': form})

# Student Management Delete view
@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('core:student_list')
    
    return render(request, 'core/student/delete_student.html', {'student': student})


@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'core/student/student_list.html', {'students': students})
         
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

    return render(request, 'core/employee/create_employee.html', {'form': form})
 
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
    
    return render(request, 'core/employee/update_employee.html', {'form': form})

# Employee Management Delete View
@login_required
def delet_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('core:employee_list')
    
    return render(request, 'core/employee/delete_employee.html', {'employee': employee})

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'core/employee/employee_list.html', {'employees': employees})

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
        return render(request, 'core/rfid/assign_rfid.html', {'form': form})

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

    return render(request, 'core/rfid/update_rfid.html', {'form': form, 'rfid_card': rfid_card})

# RFID Card Management Delete View
@login_required
def delete_rfid(request, pk):
    rfid_card = get_object_or_404(RFIDCard, pk=pk)
    if request.method == 'POST':
        rfid_card.delete()
        messages.success(request, "RFID Card deleted successfully!")
        
        return redirect('core:rfid_list') 
    return render(request, 'core/rfid/delete_rfid.html', {'rfid_card': rfid_card})


@login_required
def rfid_list(request):
    rfid_cards = RFIDCard.objects.all()
    return render(request, 'core/rfid/rfid_list.html', {'rfid_cards': rfid_cards})

# HOD views for the dashboard
@login_required
def hod_dashboard(request):
    # Ensure the user is a HOD
    if request.user.user_type != 1:
        return redirect('core:home')

    # Fetch data related to the HOD's department
    department = request.user.employee.department

    # Fetch the number of registered employees in the department
    employee_count = Employee.objects.filter(department=department).count()

    # Fetch recent employee activity (this could be replaced with actual activity tracking logic)
    recent_employees = Employee.objects.filter(department=department).order_by('-id')[:5]

    # Fetch student enrollment data in the HOD's department
    student_count = Student.objects.filter(department=department).count()

    # Fetch student attendance data for each course in the department
    attendance_data = AttendanceRecord.objects.filter(course__department=department)

    # Calculate pending approvals if there is such logic (placeholder for now)
    pending_approvals = 0  # Replace with actual pending approval logic

    context = {
        'employee_count': employee_count,
        'recent_employees': recent_employees,
        'student_count': student_count,
        'attendance_data': attendance_data,
        'pending_approvals': pending_approvals,
    }
    return render(request, 'core/dashboard/hod_dashboard.html', context)

# For lecturer
@login_required
def lecturer_dashboard(request):
    # Ensure the user is a Lecturer
    if request.user.user_type != 2:
        return redirect('core:home')

    # Fetch courses assigned to the lecturer
    courses = Course.objects.filter(lecturer=request.user)

    # Fetch upcoming exams for the lecturer's courses
    upcoming_exams = Exam.objects.filter(course__in=courses, date__gte=datetime.now())

    # Fetch recent student performance (placeholder for actual performance tracking)
    student_performance = None  # Replace with actual performance tracking logic

    # Fetch attendance records for the lecturer's courses
    attendance_records = AttendanceRecord.objects.filter(course__in=courses)

    context = {
        'courses': courses,
        'upcoming_exams': upcoming_exams,
        'student_performance': student_performance,
        'attendance_records': attendance_records,
    }
    return render(request, 'core/dashboard/lecturer_dashboard.html', context)