from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'HOD'),
        (2, 'Lecturer'),
        (3, 'Student'),
        (4, 'Employee'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)


    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def is_student(self):
        return self.user_type == 3
    
    def is_employee(self):
        return self.user_type == 4

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=50)
    student_class = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number  = models.CharField(max_length=15)
    nationality = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='data/student_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"
    
    def clean(self):
        if not self.user.is_student():
            raise ValidationError("Assigned user must be of type 'Student'.")

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    function = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='data/employee_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.function}"
    
    def clean(self):
        if not self.user.is_employee():
            raise ValidationError("Assigned user must be of type 'Employee'.")

class RFIDCard(models.Model):
    card_id = models.CharField(max_length=20, unique=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.student:
            return f"Card {self.card_id} - Student: {self.student.user.username}"
        elif self.employee:
            return f"Card {self.card_id} - Employee: {self.employee.user.username}"
        else:
            return f"Card {self.card_id} - Unassigned"
        
    def clean(self):
        if self.student and self.employee:
            raise ValidationError("RFID Card cannot be assigned to both a student and an empoyee")
        if not self.student and not self.employee:
            raise ValidationError("RFID Card must be assigned to either a student or an employee")