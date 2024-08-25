from django.shortcuts import render, get_object_or_404, redirect
from .models import Exam, ExamAttendance
from .forms import ExamAttendanceForm
from courses.models import Course

# Exam Views
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exams/exam_list.html', {'exams': exams})

def add_exam(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, id=course_id)
        date = request.POST.get('date')
        time = request.POST.get('time')
        duration = request.POST.get('duration')

        exam = Exam(course=course, date=date, time=time, duration=duration)
        exam.save()
        return redirect('exams:exam_list')

    courses = Course.objects.all()
    return render(request, 'exams/add_exam.html', {'courses': courses})

def update_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = get_object_or_404(Course, id=course_id)
        exam.course = course
        exam.date = request.POST.get('date')
        exam.time = request.POST.get('time')
        exam.duration = request.POST.get('duration')
        exam.save()
        return redirect('exams:exam_list')

    courses = Course.objects.all()
    return render(request, 'exams/update_exam.html', {'exam': exam, 'courses': courses})

def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    exam.delete()
    return redirect('exams:exam_list')

# Exam Attendance Views
def exam_attendance_list(request):
    attendances = ExamAttendance.objects.all()
    return render(request, 'exams/exam_attendance_list.html', {'attendances': attendances})

def add_exam_attendance(request):
    if request.method == 'POST':
        form = ExamAttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exams:exam_attendance_list')
    else:
        form = ExamAttendanceForm()

    return render(request, 'exams/add_exam_attendance.html', {'form': form})

def update_exam_attendance(request, attendance_id):
    attendance = get_object_or_404(ExamAttendance, id=attendance_id)

    if request.method == 'POST':
        form = ExamAttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('exams:exam_attendance_list')
    else:
        form = ExamAttendanceForm(instance=attendance)

    return render(request, 'exams/update_exam_attendance.html', {'form': form})

def delete_exam_attendance(request, attendance_id):
    attendance = get_object_or_404(ExamAttendance, id=attendance_id)
    attendance.delete()
    return redirect('exams:exam_attendance_list')
