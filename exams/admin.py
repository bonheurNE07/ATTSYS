from django.contrib import admin
from .models import Exam, ExamAttendance

admin.site.register(Exam)
admin.site.register(ExamAttendance)