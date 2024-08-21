from django.test import TestCase
from django.utils import timezone
from core.models import User, Student
from attendance.models import AttendanceRecord
from courses.models import Course

class AttendanceRecordModelTest(TestCase):

    def setUp(self):
        # create a test user (Lecture)
        self.lecturer = User.objects.create_user(username='lecture1', password='pass123', user_type=2)

        # create a test student
        self.student = Student.objects.create(
            user = User.objects.create_user(username='student1', password='pass123', user_type=3),
            roll_number='2025001',
            department='computer science',
            student_class='Year 1',
            email='student1@gmail.com',
            phone_number='0892387583',
            nationality='Rwandan',
        )

        # create a test course
        self.course = Course.objects.create(
            name='Introduction to Programming',
            code='CS101',
            credits=3,
            lecturer=self.lecturer
            )

        # create an attendance record
        self.attendance_record = AttendanceRecord.objects.create(
            student = self.student,
            course = self.course,
            date = timezone.now().date(),
            status = 'P',
            rfid_card = 'RFID123456789',
            lecturer = self.lecturer
        )

    def test_attendance_record_creation(self):
        """ Test that the attendance record is created correctly """
        record = AttendanceRecord.objects.get(id=self.attendance_record.id)
        self.assertEqual(record.student, self.student)
        self.assertEqual(record.course, self.course)
        self.assertEqual(record.status, 'P')

    def test_attendance_record_str(self):
        """ Test the string representation of the attendance record """
        record = AttendanceRecord.objects.get(id=self.attendance_record.id)
        print(str(record)) # f"{self.student} - {self.course} - {record.date} - {record.status}"
        self.assertEqual(str(record), f"{self.student} - {self.course} - {record.date} - {record.status}")