from django import forms
from .models import Student, User, RFIDCard
import re

class StudentForm(forms.ModelForm):
    rfid_card = forms.ModelChoiceField(
        queryset=RFIDCard.objects.filter(student__isnull=True), 
        required=False,
        label="RFID Card",
        help_text="Assign an RFID card to the student. This card should be unique and unassigned."
    )

    class Meta:
        model = Student
        fields = ['user', 'roll_number', 'department', 'student_class', 'email', 'phone_number', 'nationality', 'photo', 'rfid_card']
        labels = {
            'user': 'User Account',
            'roll_number': 'Roll Number',
            'department': 'Department',
            'student_class': 'Class',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'nationality': 'Nationality',
            'photo': 'Profile Photo',
        }
        help_texts = {
            'user': 'Select the user account associated with this student.',
            'roll_number': 'Enter the unique roll number for the student.',
            'email': 'Use the official university email if available.',
            'phone_number': 'Enter a valid phone number for communication.',
            'photo': 'Upload a profile photo for the student (optional).',
        }
        widgets = {
            'user': forms.Select(attrs={'placeholder': 'Select User'}),
            'roll_number': forms.TextInput(attrs={'placeholder': 'e.g., 202150126'}),
            'department': forms.TextInput(attrs={'placeholder': 'e.g., Electromagnetics Engineering 2'}),
            'student_class': forms.TextInput(attrs={'placeholder': 'e.g., ELT 201'}),
            'email': forms.EmailInput(attrs={'placeholder': 'e.g., student@gmail.com'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'e.g., 0791348888'}),
            'nationality': forms.TextInput(attrs={'placeholder': 'e.g., Rwandan'}),
            'photo': forms.ClearableFileInput(attrs={'placeholder': 'Choose Photo'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(user_type=3)  # Only students

    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number')
        if Student.objects.filter(roll_number=roll_number).exists():
            raise forms.ValidationError("This roll number is already in use.")
        return roll_number

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Add any phone number validation logic here
        return phone_number

    def save(self, commit=True):
        student = super(StudentForm, self).save(commit=False)
        rfid_card = self.cleaned_data.get('rfid_card')
        if rfid_card:
            rfid_card.student = student
            rfid_card.save()
        if commit:
            student.save()
        return student

class RFIDCardForm(forms.ModelForm):
    class Meta:
        model = RFIDCard
        fields = ['card_id', 'student']
        labels = {
            'card_id': 'RFID Card ID',
            'student': 'Assign to Student',
        }
        help_texts = {
            'card_id': 'Enter the unique RFID card ID.',
            'student': 'Select a student to assign this card to.',
        }
        widgets = {
            'card_id': forms.TextInput(attrs={'placeholder': 'e.g., 1234567890'}),
            'student': forms.Select(attrs={'placeholder': 'Select Student'}),
        }

    def __init__(self, *args, **kwargs):
        super(RFIDCardForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter(rfidcard__isnull=True)

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')

        if not student:
            raise forms.ValidationError("RFID Card must be assigned to a student.")
        
        return cleaned_data
