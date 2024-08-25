from django import forms
from .models import AttendanceRecord
from core.models import Student, Employee, User
from courses.models import Course

class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['student', 'employee', 'course', 'date', 'status', 'rfid_card', 'lecturer']
        labels = {
            'student': 'Student',
            'employee': 'Employee',
            'course': 'Course',
            'date': 'Date of Attendance',
            'status': 'Attendance Status',
            'rfid_card': 'RFID Card',
            'lecturer': 'Lecturer',
        }

        help_texts = {
            'student': 'Select the student for whom the attendance is being recorded.',
            'employee': 'Select the employee for whom the attendance is being recorded.',
            'course': 'Select the course for which the attendance is being recorded (only for students).',
            'date': 'Enter the date of attendance.',
            'status': 'Mark whether the person was present or absent.',
            'rfid_card': 'Enter the RFID card number.',
            'lecturer': 'Select the lecturer recording this attendance (only for students).',
        }

        widgets = {
            'student': forms.Select(attrs={'placeholder': 'Select Student'}),
            'employee': forms.Select(attrs={'placeholder': 'Select Employee'}),
            'course': forms.Select(attrs={'placeholder': 'Select Course'}),
            'date': forms.Select(attrs={'type': 'date'}),
            'status': forms.Select(attrs={'placeholder': 'Select Status'}),
            'rfid_card': forms.TextInput(attrs={'placeholder': 'Enter RFID Card'}),
            'lecturer': forms.Select(attrs={'placeholder': 'Select Lecturer'}),
        }

    def __init__(self, *args, **kwargs):
        super(AttendanceRecordForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.all()
        self.fields['employee'].queryset = Employee.objects.all()
        self.fields['lecturer'].queryset = User.objects.filter(user_type=2)
    
    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        employee = cleaned_data.get('employee')
        course = cleaned_data.get('course')
        date = cleaned_data.get('date')

        # Ensure that either a student or an employee is selected, but not both
        if not student and not employee:
            raise forms.ValidationError("Either a student or an employee must be selected.")
        if student and employee:
            raise forms.ValidationError("Select either a student or an employee, not both.")
        
        # Ensure course is only selected if a student is selected
        if student and not course:
            raise forms.ValidationError("Course must be selected for a student.")
        if employee and course:
            raise forms.ValidationError("Course should not be selected for an employee.")

        # Check if the attendance record already exists
        if AttendanceRecord.objects.filter(student=student, employee=employee, course=course, date=date).exists():
            raise forms.ValidationError("Attendance for this record already exists.")
        
        return cleaned_data
