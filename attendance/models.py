from django.db import models
from core.models import Student, User
from courses.models import Course

class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    rfid_card = models.CharField(max_length=20)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 2})

    class Meta:
        unique_together = ['student', 'course', 'date']

    def __str__(self):
        return f"{self.student} - {self.course} - {self.date} - {self.status}"