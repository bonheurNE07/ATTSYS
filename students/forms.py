from django import forms
from .models import Enrollment

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'completion_status']
        labels = {
            'student': 'Student',
            'course': 'Course',
            'completion_status': 'Completion Status',
        }

        help_texts = {
            'student': 'Select the student enrolling in this course.',
            'course': 'Select the course the student is enrolling in.',
            'completion_status': 'Indicate whetger the course is ngoing or completed.',
        }
        
        widgets = {
            'student': forms.Select(attrs={'placeholder': 'Select Student'}),
            'course': forms.Select(attrs={'placeholder': 'Select Course'}),
            'completion_status': forms.Select(attrs={'placeholder': 'Select Status'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            student = cleaned_data.get('student')
            course = cleaned_data.get('course')

            if Enrollment.objects.filter(student=student, course=course).exists():
                raise forms.ValidationError(f"{student} is already enrolled in {course}.")
            
            return cleaned_data