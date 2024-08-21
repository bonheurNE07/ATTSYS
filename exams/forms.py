from django import forms
from .models import ExamAttendance

class ExamAttendanceForm(forms.ModelForm):
    class Meta:
        model = ExamAttendance
        fields = ['student', 'exam', 'status', 'rfid_card', 'recorded_by']
        labels = {
            'student': 'Student',
            'exam': 'Exam',
            'status': 'Attendance Status',
            'rfid_card': 'RFID Card',
            'recorded_by': 'Recorded By',
        }
        help_texts = {
            'student': 'Select the student for whom this attendance is being recorded.',
            'exam': 'Select the exam for which the attendance is being recorded.',
            'status': 'Mark the student as Present (P) or Absent (A).',
            'rfid_card': 'Enter the RFID card used to register attendance.',
            'recorded_by': 'The finance employee recording this attendance.',
        }
        widgets = {
            'student': forms.Select(attrs={'placeholder': 'Select Student'}),
            'exam': forms.Select(attrs={'placeholder': 'Select Exam'}),
            'status': forms.Select(attrs={'placeholder': 'Select Status'}),
            'rfid_card': forms.TextInput(attrs={'placeholder': 'Enter RFID Card ID'}),
            'recorded_by': forms.Select(attrs={'placeholder': 'Select Finance Employee'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        exam = cleaned_data.get('exam')

        if ExamAttendance.objects.filter(student=student, exam=exam).exists():
            raise forms.ValidationError("Attendance for this student in this exam has already been recorded.")

        return cleaned_data

    def clean_rfid_card(self):
        rfid_card = self.cleaned_data.get('rfid_card')
        if not rfid_card:
            raise forms.ValidationError("RFID Card is required to record attendance.")
        return rfid_card