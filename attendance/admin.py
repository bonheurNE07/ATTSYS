from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status', 'rfid_card', 'lecturer')
    list_filter = ('course', 'date', 'status')
    search_fields = ('student__user__username', 'course__name', 'lecture__username', 'rfid_card')
    ordering = ('-date',)

