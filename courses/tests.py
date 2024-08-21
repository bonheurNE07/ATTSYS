from django.test import TestCase
from core.models import User
from courses.models import Course

class CourseRecordTest(TestCase):

    def setUp(self):
        # create a test user (Lecture) type 2
        self.lecturer = User.objects.create(username='lecture2', password='12345678pass', user_type=2)

        self.course = Course.objects.create(
            name = 'Physics 2',
            code = 'CS502',
            credits = 4,
            lecturer = self.lecturer
        )

    def test_course_creation(self):
        """Test if the course is created correctly """
        record = Course.objects.get(id=self.course.id)
        self.assertEqual(record.name, 'Physics 2')
        self.assertEqual(record.code, 'CS502')
        self.assertEqual(record.credits, 4)
        self.assertEqual(record.lecturer, self.lecturer)
    
    def test_course_record_str(self):
        """Test the string representation of the course creation record"""
        record = Course.objects.get(id=self.course.id)
        self.assertEqual(str(record), f"{self.course}")