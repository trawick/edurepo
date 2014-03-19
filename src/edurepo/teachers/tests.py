from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from models import Teacher, TeacherClass


class BasicTests(TestCase):

    def setUp(self):
        self.email1 = 'trawick@example.com'
        self.name1 = 'Jeff T'

        self.u1 = User.objects.create_user(username='user1', email='user1@example.com')
        self.t1 = Teacher(email=self.email1, name=self.name1, user=self.u1)
        self.t1.save()

        self.good_provider = 'http://127.0.0.1:8080/'
        self.bad_provider = 'http://127.0.0.1:8081/'

        self.good_course = 'MG4'
        self.bad_course = 'xxx' + self.good_course + 'xxx'

    def test_1(self):
        """Basic creation/update of Teacher"""
        email = 'trawick@example.com'
        name1 = 'Jeff'
        name2 = 'Jeff T'
        t1 = Teacher(email=email, name=name1, user=self.u1)
        t1.save()
        t2 = Teacher(email=email, name=name2, user=self.u1)
        t2.save()

        obj = Teacher.objects.get(email=email)
        self.assertEquals(obj.name, name2)

    def test_good_repo_and_course_id(self):
        tc = TeacherClass(name='1st period math',
                          course_id=self.good_course, teacher=self.t1,
                          repo_provider=self.good_provider)
        tc.save()

    def test_good_repo_and_bad_course_id(self):
        tc = TeacherClass(name='1st period math',
                          course_id=self.bad_course, teacher=self.t1,
                          repo_provider=self.good_provider)
        self.assertRaises(ValidationError, lambda: tc.save())

    def test_bad_repo_and_good_course_id(self):
        tc = TeacherClass(name='1st period math',
                          course_id=self.good_course, teacher=self.t1,
                          repo_provider=self.bad_provider)
        self.assertRaises(ValidationError, lambda: tc.save())
