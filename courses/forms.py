from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'credits', 'lecturer']
        labels = {
            'name': 'Course Name',
            'code': 'Course Code',
            'description': 'Course Description',
            'credits': 'ECredits',
            'lecturer': 'Lecturer',
        }

        help_texts = {
            'name': 'Enter the full name of the course.',
            'code': 'Enter the unique course code (e.g., ELT 201).',
            'description': 'Provide a brief description of this course.',
            'credits': 'Enter the number of credits for this course.',
            'lecturer': 'Select the lecturer responsible for this course.',
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder':'e.g., '}),
            'code': forms.TextInput(attrs={'placeholder':'e.g., '}),
            'descriptions': forms.TextInput(attrs={'placeholder':'e.g., '}),
            'credits': forms.TextInput(attrs={'placeholder':'e.g., '}),
            'lecturer': forms.TextInput(attrs={'placeholder':'e.g., '})
        }

    def clean(self):
        code = self.cleaned_data.get('code')
        if Course.objects.filter(code=code).exists():
            raise forms.ValidationError("This course code is already in use.")
        return code
    
    def clean_credits(self):
        credits = self.cleaned_data.get('credits')
        if credits <= 0:
            raise forms.ValidationError("Credits must be a positive number.")
        return credits