from django.db import models
from core.models import Student, User
from courses.models import Course

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField()

    def __str__(self) -> str:
        return f"{self.course} - {self.date} - {self.time}"
    
class ExamAttendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam =  models.ForeignKey(Exam, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    rfid_card = models.CharField(max_length=20)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'usertype':4}) # Finance Employee only

    class Meta:
        unique_together = ['student', 'exam']
    
    def __str__(self) -> str:
        return f"{self.student} - {self.exam} - {self.status}"