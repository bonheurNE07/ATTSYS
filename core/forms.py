from django import forms
from .models import Student, Employee, User, RFIDCard
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


class EmployeeForm(forms.ModelForm):
    rfid_card = forms.ModelChoiceField(
        queryset=RFIDCard.objects.filter(employee__isnull=True), 
        required=False,
        label="RFID Card",
        help_text="Assign an RFID card to the employee. This card should be unique and unassigned."
    )

    class Meta:
        model = Employee
        fields = ['user', 'function', 'department', 'phone_number', 'email', 'photo', 'rfid_card']
        labels = {
            'user': 'User Account',
            'function': 'Function',
            'department': 'Department',
            'phone_number': 'Phone Number',
            'email': 'Email Address',
            'photo': 'Profile Photo',
        }
        help_texts = {
            'user': 'Select the user account associated with this employee.',
            'function': 'Enter the job function of the employee.',
            'department': 'Specify the department where the employee works.',
            'phone_number': 'Enter a valid phone number for communication.',
            'email': 'Use the official university email.',
            'photo': 'Upload a profile photo for the employee (optional).',
        }
        widgets = {
            'user': forms.Select(attrs={'placeholder': 'Select User'}),
            'function': forms.TextInput(attrs={'placeholder': 'e.g., Lecturer'}),
            'department': forms.TextInput(attrs={'placeholder': 'e.g., Computer Science'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'e.g., 0791348888'}),
            'email': forms.EmailInput(attrs={'placeholder': 'e.g., employee@ulk.ac.rw'}),
            'photo': forms.ClearableFileInput(attrs={'placeholder': 'Choose Photo'}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(user_type=4)  # Only employees

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith("@ulk.ac.rw"):
            raise forms.ValidationError("Please use a valid ULK university email address.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Regular expressions for Rwandan and DRC phone numbers
        rwandan_pattern = re.compile(r'^\+2507[2,3,8][0-9]{7}$')
        drc_pattern = re.compile(r'^\+243(97|79)[0-9]{7}$')

        if not (rwandan_pattern.match(phone_number) or drc_pattern.match(phone_number)):
            raise forms.ValidationError("Please enter a valid Rwandan or DRC phone number.")

        return phone_number

    def save(self, commit=True):
        employee = super(EmployeeForm, self).save(commit=False)
        rfid_card = self.cleaned_data.get('rfid_card')
        if rfid_card:
            rfid_card.employee = employee
            rfid_card.save()
        if commit:
            employee.save()
        return employee
    
class RFIDCardForm(forms.ModelForm):
    class Meta:
        model = RFIDCard
        fields = ['card_id', 'student', 'employee']
        labels = {
            'card_id': 'RFID Card ID',
            'student': 'Assign to Student',
            'employee': 'Assign to Employee',
        }
        help_texts = {
            'card_id': 'Enter the unique RFID card ID.',
            'student': 'Select a student to assign this card to.',
            'employee': 'Select an employee to assign this card to.',
        }
        widgets = {
            'card_id': forms.TextInput(attrs={'placeholder': 'e.g., 1234567890'}),
            'student': forms.Select(attrs={'placeholder': 'Select Student'}),
            'employee': forms.Select(attrs={'placeholder': 'Select Employee'}),
        }

    def __init__(self, *args, **kwargs):
        super(RFIDCardForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter(rfidcard__isnull=True)
        self.fields['employee'].queryset = Employee.objects.filter(rfidcard__isnull=True)

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        employee = cleaned_data.get('employee')

        if student and employee:
            raise forms.ValidationError("RFID Card cannot be assigned to both a student and an employee.")
        if not student and not employee:
            raise forms.ValidationError("RFID Card must be assigned to either a student or an employee.")
        
        return cleaned_data
