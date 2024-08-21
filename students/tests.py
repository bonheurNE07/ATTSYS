from django.test import TestCase
from core.models import Student, User
from courses.models import Course
from exams.models import Exam, ExamAttendance
from students.models import Enrollment
from datetime import timedelta

class EnrollementModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            user = User.objects.create_user(username='student1', user_type=3),
            roll_number='202150126',
            department='Computer Science',
            student_class='CS50201',
            email='Student1@gmail.com',
            phone_number='0791348888',
            nationality='Congolese'
        )

        self.course = Course.objects.create(
            name='Data Structure',
            code='CS201',
            credits=4,
            lecturer=User.objects.create_user(username='lecture1', user_type=2)
        )
        self.enrollment = Enrollment.objects.create(student=self.student, course=self.course,completion_status='ongoing')

    def test_enrollment_creation(self):
        self.assertEqual(self.enrollment.student, self.student)
        self.assertEqual(self.enrollment.course, self.course)
        self.assertEqual(self.enrollment.completion_status, 'ongoing')

class ExamAttendanceModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            user = User.objects.create_user(username='student1', user_type=3),
            roll_number='202150126',
            department='Computer Science',
            student_class='CS50201',
            email='Student1@gmail.com',
            phone_number='0791348888',
            nationality='Congolese'
        )

        self.exam = Exam.objects.create(
            course=Course.objects.create(
                name='Algprithms',
                code='CS301',
                credits=4,
                lecturer=User.objects.create_user(username='lecturer2', user_type=2)
            ),
            date='2024-08-25',
            time='09:00:00',
            duration=timedelta(hours=3)
        )

        self.finance_employee = User.objects.create_user(username='finance1', user_type=4)
        self.exam_attendance = ExamAttendance.objects.create(
            student=self.student,
            exam=self.exam,
            status='P',
            rfid_card='1234567890',
            recorded_by=self.finance_employee
        )

    def test_exam_attendance_creation(self):
        self.assertEqual(self.exam_attendance.student, self.student)
        self.assertEqual(self.exam_attendance.exam, self.exam)
        self.assertEqual(self.exam_attendance.status, 'P')
        self.assertEqual(self.exam_attendance.recorded_by, self.finance_employee)