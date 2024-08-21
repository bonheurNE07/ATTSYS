from django import forms
from .models import AttendanceRecord
from core.models import Student, User
from courses.models import Course

class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['student', 'course', 'date', 'status', 'rfid_card', 'lecture']
        labels = {
            'student': 'Student',
            'course': 'Course',
            'date': 'Date of Attendance',
            'status': 'Attendance Status',
            'rfid_card': 'RFID Card',
            'lecturer': 'Lecturer',
        }

        help_texts = {
            'student': 'Select the student for whom the attendance is being recorded.',
            'course': 'Select the course for which the attendance is being recorded.',
            'date': 'Enter the date of the class.',
            'status': 'Mark whether the student was present or absent.',
            'rfid_card': 'Enter the RFID card number used by the student.',
            'lecturer': 'Select the lecturer recording this attendance.',
        }

        widgets = {
            'student': forms.Select(attrs={'placeholder': 'Select Student'}),
            'course': forms.Select(attrs={'placeholder': 'Select Course'}),
            'date': forms.Select(attrs={'type': 'date'}),
            'status': forms.Select(attrs={'placeholder': 'Select Status'}),
            'rfid_card': forms.Select(attrs={'placeholder': 'Enter RFID Card'}),
            'lecturer': forms.Select(attrs={'placeholder': 'Select Lecturer'}),
        }

    def __init__(self, *args, **kwargs):
        super(AttendanceRecordForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.all()
        self.fields['lecturer'].queryset = User.objects.filter(user_type=2)
    
    def clean(self):
        cleanned_date = super().clean()
        student = cleanned_date.get('student')
        course = cleanned_date.get('course')
        date = cleanned_date.get('date')

        # Check if the atttendance record already exists
        if AttendanceRecord.objects.filter(student=student, course=course, date=date).exists():
            raise forms.ValidationError("Attendance for this student in this course on this date has already been recorded.")
        
        return cleanned_date
