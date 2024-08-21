from django.db import models
from core.models import User

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    credits = models.PositiveSmallIntegerField()
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type':2})

    def __str__(self):
        return f"{self.name} ({self.code})"
