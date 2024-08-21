from django.contrib import admin
from .models import Student, Employee, RFIDCard, User

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'department', 'student_class', 'email', 'phone_number', 'nationality', 'photo')
    search_fields = ('roll_number', 'user__username', 'email')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user',  'function', 'department', 'phone_number', 'email', 'photo')
    search_fields = ('user__username', 'email')

admin.site.register(Student, StudentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(RFIDCard)
admin.site.register(User)