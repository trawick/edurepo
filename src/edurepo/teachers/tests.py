import datetime
import os
import unittest

from django.core.exceptions import ValidationError
from django.test import LiveServerTestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from models import Entry, Teacher, TeacherClass


class BasicTests(LiveServerTestCase):

    def setUp(self):
        if 'TEST_PROVIDER' in os.environ:
            self.good_provider = os.environ['TEST_PROVIDER']
        else:
            # This is the default server thread started by django test,
            # but it only works for this app.
            self.good_provider = 'http://localhost:8081/'  # default
        self.bad_provider = 'http://127.0.0.1:65535/'

        self.teacher_data = [('trawick@example.com', 'Jeff T', [['MG4', '1st period math', TeacherClass()]]),
                             ('jones@example.com', 'Jeff J', [['MG4', '5th period math', TeacherClass()]])]
        self.email1 = self.teacher_data[0][0]
        self.name1 = self.teacher_data[0][1]

        self.u1_password = 'F00LI5H'
        self.u1 = User.objects.create_user(username='user1', email='user1@example.com',
                                           password=self.u1_password)
        user = authenticate(username=self.u1.username, password=self.u1_password)
        assert user

        self.teachers = []
        for teacher_email, teacher_name, teacher_classes in self.teacher_data:
            t = Teacher(email=teacher_email, name=teacher_name, user=self.u1)
            t.full_clean()
            t.save()
            self.teachers.append(t)

            for i in range(len(teacher_classes)):
                course_id, class_name, _ = teacher_classes[i]
                c = TeacherClass(name=class_name,
                                 course_id=course_id,
                                 teacher=t,
                                 repo_provider=self.good_provider)
                c.full_clean()
                c.save()
                teacher_classes[i][2] = c

        # create a calendar entry for the 2nd teacher
        teacher_2 = self.teacher_data[1]
        teacher_2_class = teacher_2[2][0][2]
        e1 = Entry(teacher=self.teachers[1], teacher_class=teacher_2_class, date=datetime.date.today(),
                   objective='MG4-FACTMULT')
        e1.full_clean()
        e1.save()

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

    # This test case requires a working API provider, including
    # the repo API.  That won't work when using the server thread
    # started by django test.
    @unittest.skipIf(not 'TEST_PROVIDER' in os.environ,
                     "Test case can't work without TEST_PROVIDER pointing to API provider")
    def test_good_repo_and_course_id(self):
        tc = TeacherClass(name='1st period math (TGRC)',
                          course_id=self.good_course, teacher=self.teachers[0],
                          repo_provider=self.good_provider)
        tc.full_clean()
        tc.save()

    def test_good_repo_and_bad_course_id(self):
        tc = TeacherClass(name='1st period math (TGRBC)',
                          course_id=self.bad_course, teacher=self.teachers[0],
                          repo_provider=self.good_provider)
        self.assertRaises(ValidationError, lambda: tc.full_clean())

    def test_bad_repo_and_good_course_id(self):
        tc = TeacherClass(name='1st period math (TBRGC)',
                          course_id=self.good_course, teacher=self.teachers[0],
                          repo_provider=self.bad_provider)
        self.assertRaises(ValidationError, lambda: tc.full_clean())

    @unittest.skipIf(not 'TEST_PROVIDER' in os.environ,
                     "Test case can't work without TEST_PROVIDER pointing to API provider")
    def test_duplicate_class(self):
        name = '1st period math (TDC)'
        teacher = self.teachers[0]
        tc1 = TeacherClass(name=name, teacher=teacher,
                           course_id=self.good_course,
                           repo_provider=self.good_provider)
        tc1.full_clean()
        tc1.save()
        tc2 = TeacherClass(name=name, teacher=teacher,
                           course_id=self.good_course,
                           repo_provider=self.good_provider)
        self.assertRaises(ValidationError, lambda: tc2.full_clean())

    @unittest.skipIf(not 'TEST_PROVIDER' in os.environ,
                     "Test case can't work without TEST_PROVIDER pointing to API provider")
    def test_duplicate_class_objective(self):
        tc = TeacherClass(name='1st period math (TDCO)',
                          course_id=self.good_course, teacher=self.teachers[0],
                          repo_provider=self.good_provider)
        tc.full_clean()
        tc.save()

        same_class = tc
        same_day = datetime.date.today()
        same_objective = 'MG4-FACTMULT'
        e1 = Entry(teacher=self.teachers[0], teacher_class=same_class, date=same_day,
                   objective=same_objective)
        e1.full_clean()
        e1.save()
        e2 = Entry(teacher=self.teachers[0], teacher_class=same_class, date=same_day,
                   objective=same_objective)
        self.assertRaises(ValidationError, lambda: e2.full_clean())

    def test_index(self):
        response = self.client.get('/teachers/')
        self.assertContains(response, self.name1, status_code=200, html=False)

    def test_detail(self):
        response = self.client.get('/teachers/' + self.email1 + '/')
        self.assertContains(response, self.name1, status_code=200, html=False)

    def test_events_empty(self):
        teacher_data = self.teacher_data[0]
        teacher_email = teacher_data[0]
        class_data = teacher_data[2][0]
        class_name = class_data[1]
        response = self.client.get('/teachers/' + teacher_email + '/' + class_name + '/')
        self.assertContains(response, 'No calendar entries for ' + class_name, status_code=200)

    @unittest.skipIf(not 'TEST_PROVIDER' in os.environ,
                     "Test case can't work without TEST_PROVIDER pointing to API provider")
    def test_events_nonempty(self):
        teacher_data = self.teacher_data[1]
        teacher_email = teacher_data[0]
        class_data = teacher_data[2][0]
        class_name = class_data[1]
        response = self.client.get('/teachers/' + teacher_email + '/' + class_name + '/')
        self.assertContains(response, 'MG4-FACTMULT', status_code=200)

    @unittest.skipIf(not 'TEST_PROVIDER' in os.environ,
                     "Test case can't work without TEST_PROVIDER pointing to API provider")
    def test_register_teacher(self):
        login = self.client.login(username=self.u1.username, password=self.u1_password)
        self.assertTrue(login)
        register_url = '/teachers/register/'
        response = self.client.get(register_url, follow=True)
        self.assertContains(response, 'Register as a teacher', status_code=200)
        response = self.client.post(register_url, {'email': 'foo@example.com',
                                                   'name': 'Ms. Smith'}, follow=True)
        self.assertContains(response, 'Edjective.org reference views', status_code=200)

        # Add a class using class just registered
        add_url = '/teachers/foo@example.com/add'
        response = self.client.get(add_url, follow=True)
        self.assertContains(response, 'Add a class', status_code=200)
        response = self.client.post(add_url, {'name': 'MyClass',
                                              'course_id': 'MG4',
                                              'repo_provider': os.environ['TEST_PROVIDER']},
                                    follow=True)
        self.assertContains(response, 'Edjective.org reference views', status_code=200)
