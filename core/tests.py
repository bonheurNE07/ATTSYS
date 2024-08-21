from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Student, Employee, User
from django.conf import settings

import os
import tempfile
import shutil

class StudentModelTest(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def setUp(self):
        self.user = User.objects.create_user(username='student1', user_type=3)
        self.student = Student.objects.create(
            user=self.user,
            roll_number='202150126',
            department='Computer Science',
            student_class='CS50120',
            email='student1@gmail.com',
            phone_number='0791348888',
            nationality='Congolese',
            photo=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

    def test_student_creation_with_photo(self):
        self.assertEqual(self.student.user.username, 'student1')
        self.assertTrue(self.student.photo.name.startswith('data/student_photos/test_image'))

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)

class EmployeeModelTest(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def setUp(self):
        self.user = User.objects.create_user(username='employee1', user_type=4)
        self.employee = Employee.objects.create(
            user=self.user,
            function='security Guard',
            department='Security',
            phone_number='0987562728',
            email='employee1@example.com',
            photo=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )
    def tearDown(self):
        # Remove the temporary MEDIA_ROOT directory
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
    def test_employee_creation_with_photo(self):
        self.assertEqual(self.employee.user.username, 'employee1')
        self.assertTrue(self.employee.photo.name.startswith('data/employee_photos/test_image'))