from django import forms
from .models import Employee
from core.models import RFIDCard, User
import re

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
