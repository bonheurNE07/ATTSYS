from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'lecturer', 'credits')
    search_fields = ('name', 'code', 'lecturer__username')
    list_filter = ('credits', 'lecturer')
