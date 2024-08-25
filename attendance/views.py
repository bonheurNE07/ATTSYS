from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from core.models import RFIDCard, Student, Employee
from courses.models import Course
from .models import AttendanceRecord
from django.utils import timezone


# View to display attendance records
@login_required
def attendance_list(request):
    if request.user.is_hod:
        attendance_records = AttendanceRecord.objects.filter(course__department=request.user.department)
    elif request.user.is_lecturer:
        attendance_records = AttendanceRecord.objects.filter(lecturer=request.user)
    elif request.user.is_employee:
        attendance_records = AttendanceRecord.objects.filter(employee=request.user.employee)
    else:
        attendance_records = AttendanceRecord.objects.none()

    context = {
        'attendance_records': attendance_records,
    }
    return render(request, 'attendance/attendance_list.html', context)

# Automatic Attendance Recording via RFID
@csrf_exempt
@login_required
def record_attendance(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        rfid_card = get_object_or_404(RFIDCard, card_id=card_id)

        if rfid_card.student:
            student = rfid_card.student
            course = None  # Retrieve or determine the course if needed
            attendance_record = AttendanceRecord.objects.create(
                student=student,
                course=course,  # Assign the appropriate course
                date=timezone.now(),
                status='Present',
                lecturer=request.user  # Assign the lecturer taking the attendance
            )
            return JsonResponse({'status': 'success', 'message': f'Attendance recorded for student {student.user.username}'})
        
        elif rfid_card.employee:
            employee = rfid_card.employee
            # Handle attendance for employees if needed (e.g., for gate attendance)
            return JsonResponse({'status': 'success', 'message': f'Attendance recorded for employee {employee.user.username}'})
        
        else:
            return JsonResponse({'status': 'error', 'message': 'RFID card is unassigned.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

# View to create attendance records manually
@login_required
def manual_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        attendance_record, created = AttendanceRecord.objects.get_or_create(
            student=student,
            course=course,
            date=timezone.now(),
            defaults={'status': 'Present', 'lecturer': request.user},
        )

        if created:
            messages.success(request, f'Attendance recorded for {student.user.username} in course {course.name}.')
        else:
            messages.info(request, f'Attendance for {student.user.username} in course {course.name} already exists.')

        return redirect('attendance:attendance_list')

    students = Student.objects.all()
    courses = Course.objects.all()
    context = {
        'students': students,
        'courses': courses,
    }
    return render(request, 'attendance/manual_attendance.html', context)

# View to display attendance details for a specific student
@login_required
def attendance_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    attendance_records = AttendanceRecord.objects.filter(student=student)

    context = {
        'student': student,
        'attendance_records': attendance_records,
    }
    return render(request, 'attendance/attendance_detail.html', context)

# View to generate attendance reports
@login_required
def attendance_report(request):
    if request.user.is_hod:
        # Generate report based on the department
        students = Student.objects.filter(department=request.user.department)
    elif request.user.is_lecturer:
        # Generate report based on the courses assigned to the lecturer
        courses = Course.objects.filter(lecturer=request.user)
        students = Student.objects.filter(course__in=courses)
    else:
        students = Student.objects.none()

    context = {
        'students': students,
    }
    return render(request, 'attendance/attendance_report.html', context)

