from django.db import models
from core.models import User
from django.core.exceptions import ValidationError

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
