from django.core.exceptions import ValidationError
from django.db import DataError, IntegrityError, transaction
from django.test import TestCase

from models import Course, CourseCategory, GlossaryItem, LearningObjective, MultipleChoiceItem, ReferenceText
from remove import delete_course
from repo.management.commands.import_xml import start_import

dummy_category_id = 'TESTNA'
dummy_category_description = 'Test Non-Academic'
dummy_course_id = 'Course00'
dummy_course_id_2 = 'Course01'
dummy_course_description = 'Course00Desc'
dummy_course_description_2 = 'Course01Desc'
dummy_objective_id = 'C00LO00'
dummy_objective_description = 'XX_C00LO00_XX'
dummy_reference_text = 'XX_C00LO00_REFERENCE_TEXT_XX'
dummy_objective_id_2 = 'C00LO01'
dummy_objective_description_2 = 'XX_C00LO01_XX'


class BasicTests(TestCase):

    def setUp(self):
        self.cc0 = CourseCategory(id=dummy_category_id, description=dummy_category_description)
        self.cc0.full_clean()
        self.cc0.save()
        self.c0 = Course(id=dummy_course_id, cat=self.cc0, description=dummy_course_description)
        self.c0.full_clean()
        self.c0.save()
        self.lo0 = LearningObjective(id=dummy_objective_id, course=self.c0, description=dummy_objective_description)
        self.lo0.full_clean()
        self.lo0.save()
        self.ref0 = ReferenceText(learning_objective=self.lo0, text=dummy_reference_text)
        self.ref0.full_clean()
        self.ref0.save()
        self.lo1 = LearningObjective(id=dummy_objective_id_2, course=self.c0, description=dummy_objective_description_2)
        self.lo1.full_clean()
        self.lo1.save()

    def test_import(self):
        for fn in ['00cat.xml', 'M/grade4.xml', 'M/mg4-mc.xml', 'M/mg4-tf.xml']:
            start_import('../../samples/' + fn, 'check', spew=False)
            start_import('../../samples/' + fn, 'import', spew=False)

        objects = CourseCategory.objects.filter(id='K12-SS')
        self.assertEquals(len(objects), 1)
        objects = Course.objects.filter(id='MG4')
        self.assertEquals(len(objects), 1)

        delete_course('MG4', delete=True, noisy=False)
        objects = Course.objects.filter(id='MG4')
        self.assertEquals(len(objects), 0)

    def test_1(self):
        """Basic creation/update of Course and default language"""
        course_id = dummy_course_id_2
        c1 = Course(id=course_id, cat=self.cc0, description=dummy_course_description_2)
        self.assertEquals(c1.language, 'en')
        c1.save()

        desc2 = 'desc2'
        c2 = Course(id=course_id, cat=self.cc0, description=desc2)
        c2.save()

        obj = Course.objects.get(id=course_id)
        self.assertEquals(obj.description, desc2)

        self.assertEquals(obj.language, 'en')

    def test_duplicate_glossary_item(self):
        gi1 = GlossaryItem(term='term01', learning_objective=self.lo0)
        gi1.save()

        gi2 = GlossaryItem(term='term01', learning_objective=self.lo0)
        self.assertRaises(IntegrityError, lambda: gi2.save())

    def test_id_syntax(self):
        with self.assertRaises(DataError):
            with transaction.atomic():
                tis_cc0 = CourseCategory(id='123456789', description='too long')
                tis_cc0.save()

        with self.assertRaises(ValidationError):
            with transaction.atomic():
                tis_cc1 = CourseCategory(id='has spc', description='will not work')
                tis_cc1.full_clean()

        with self.assertRaises(ValidationError):
            with transaction.atomic():
                tis_c0 = Course(id='has space', cat=self.cc0, description='who cares')
                tis_c0.full_clean()

        with self.assertRaises(ValidationError):
            with transaction.atomic():
                tis_lo0 = LearningObjective(id='has space', course=self.c0, description='foobar')
                tis_lo0.full_clean()

    def test_multiple_choice_constraints(self):
        tmcc_1 = MultipleChoiceItem(learning_objective=self.lo0,
                                    question='ABC?',
                                    choice1='xxx',
                                    choice2='yyy',
                                    type=1,
                                    ans=1)
        tmcc_1.full_clean()
        self.assertEqual(tmcc_1.language, 'en', 'Language did not default to "en"')

        # bad value for type
        with self.assertRaises(ValidationError):
            with transaction.atomic():
                tmcc_2 = MultipleChoiceItem(learning_objective=self.lo0,
                                            question='ABC?',
                                            choice1='xxx',
                                            choice2='yyy',
                                            type=7,
                                            ans=1)
                tmcc_2.full_clean()

        # question too long
        with self.assertRaises(ValidationError):
            with transaction.atomic():
                tmcc_3 = MultipleChoiceItem(learning_objective=self.lo0,
                                            question='1' * 401,
                                            choice1='xxx',
                                            choice2='yyy',
                                            type=7,
                                            ans=1)
                tmcc_3.full_clean()

    def test_index(self):
        response = self.client.get("/repo/")
        self.assertContains(response, dummy_course_id)

    def test_detail(self):
        response = self.client.get("/repo/" + dummy_course_id + "/")
        self.assertContains(response, dummy_objective_id)

    def test_by_objective(self):
        response = self.client.get("/repo/" + dummy_course_id + "/" + dummy_objective_id + "/")
        self.assertContains(response, dummy_objective_description)
        self.assertContains(response, dummy_reference_text)
