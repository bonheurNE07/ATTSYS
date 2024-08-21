from django.test import TestCase
from core.models import Student, User
from courses.models import Course
from .models import Exam, ExamAttendance
from datetime import time, timedelta

class ExamModelTest(TestCase):
    def setUp(self):
        self.lecturer = User.objects.create_user(username='lecture1', user_type=2)
        self.course = Course.objects.create(name='Dat Structure', code='CS201', credits=4, lecturer=self.lecturer)
        self.exam = Exam.objects.create(course=self.course, date='2024-08-25', time='09:00:00', duration=timedelta(hours=3))

    def test_exam_creation(self):
        self.assertEqual(self.exam.course, self.course)
        self.assertEqual(self.exam.date, '2024-08-25')
        self.assertEqual(self.exam.time, str(time(9, 0)))
        self.assertEqual(self.exam.duration, timedelta(hours=3))

class ExamAttendanceModelTest(TestCase):
    def setUp(self):
        self.lecturer = User.objects.create_user(username='lecture1', user_type=2)
        self.course = Course.objects.create(name='Dat Structure', code='CS201', credits=3, lecturer=self.lecturer)
        self.exam = Exam.objects.create(course=self.course, date='2024-08-25', time='09:00:00', duration=timedelta(hours=3))

        self.student = Student.objects.create(user=User.objects.create_user(username='student1', user_type=3))
        self.finance_employee = User.objects.create_user(username='finance1', user_type=4)
        self.attendance = ExamAttendance.objects.create(student=self.student, exam=self.exam, status='P', rfid_card='1234567890', recorded_by=self.finance_employee)

    def test_exam_attendance_creation(self):
        self.assertEqual(self.attendance.student, self.student)
        self.assertEqual(self.attendance.exam, self.exam)
        self.assertEqual(self.attendance.status, 'P')
