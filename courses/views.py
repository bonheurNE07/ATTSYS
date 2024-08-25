from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from .forms import CourseForm

# View to display all courses
@login_required
def course_list(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'courses/course_list.html', context)

# View to display details of a specific course
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    context = {
        'course': course,
    }
    return render(request, 'courses/course_detail.html', context)

# View to create a new course
@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully!')
            return redirect('courses:course_list')
    else:
        form = CourseForm()
    context = {
        'form': form,
    }
    return render(request, 'courses/course_form.html', context)

# View to update an existing course
@login_required
def course_update(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('courses:course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'courses/course_form.html', context)

# View to delete a course
@login_required
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('courses:course_list')
    context = {
        'course': course,
    }
    return render(request, 'courses/course_confirm_delete.html', context)
