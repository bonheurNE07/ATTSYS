from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Enrollment
from .forms import EnrollmentForm
from core.models import Student

# View to display a list of all enrollments
@login_required
def enrollment_list(request):
    enrollments = Enrollment.objects.all()
    context = {
        'enrollments': enrollments,
    }
    return render(request, 'students/enrollment_list.html', context)

# View to add a new enrollment
@login_required
def add_enrollment(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enrollment added successfully!')
            return redirect('students:enrollment_list')
    else:
        form = EnrollmentForm()

    context = {
        'form': form,
    }
    return render(request, 'students/add_enrollment.html', context)

# View to edit an existing enrollment
@login_required
def edit_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enrollment updated successfully!')
            return redirect('students:enrollment_list')
    else:
        form = EnrollmentForm(instance=enrollment)

    context = {
        'form': form,
        'enrollment': enrollment,
    }
    return render(request, 'students/edit_enrollment.html', context)

# View to delete an enrollment
@login_required
def delete_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Enrollment deleted successfully!')
        return redirect('students:enrollment_list')

    context = {
        'enrollment': enrollment,
    }
    return render(request, 'students/delete_enrollment.html', context)

# View to show detailed enrollment information for a specific student
@login_required
def student_enrollment_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    enrollments = Enrollment.objects.filter(student=student)

    context = {
        'student': student,
        'enrollments': enrollments,
    }
    return render(request, 'students/student_enrollment_detail.html', context)
