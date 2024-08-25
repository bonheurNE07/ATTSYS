from django.db import models
from core.models import Student, User, Employee  # Assuming you have an Employee model
from courses.models import Course

class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)  # Only for students
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    rfid_card = models.CharField(max_length=20)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 2}, null=True, blank=True)  # For students

    class Meta:
        unique_together = ['student', 'employee', 'course', 'date']

    def __str__(self):
        return f"{self.student or self.employee} - {self.course} - {self.date} - {self.status}"
