from django.db import models
from core.models import Student, User
from courses.models import Course

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    completion_status = models.CharField(max_length=20, choices=[("ongoing", "Ongoing"),("completed", "Completed")])


    def __str__(self):
        return f"{self.student} enrolled in {self.course}"
    
