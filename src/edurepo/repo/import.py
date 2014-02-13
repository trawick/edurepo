import os
import sys
from xml.etree.ElementTree import parse
from repo.models import Course, LearningObjective, GlossaryItem, TrueFalseItem

def import_course_standard(root):
    print 'Course standard: %s' % root.get('id')

    description = root.find('description')
    print description.text

    # don't care about <source></source> for now

    objectives = root.find('objectives')

    for child in objectives:
        print 'Objective: %s' % child.get('id')
        print '  %s' % child.find('description').text


def import_tf_questions(root):
    for obj_group in root.findall('objective-group'):
        obj_id = obj_group.find('objective-id').text
        print 'T-F questions for objective %s:' % obj_id
        for question in obj_group.findall('question'):
            print '  %s (%s)' % (question.find('statement').text, question.find('answer').text)


def import_glossary_items(root):
    for obj_group in root.findall('objective-group'):
        obj_id = obj_group.find('objective-id').text
        print 'Glossary items for objective %s:' % obj_id
        for item in obj_group.findall('item'):
            print '  %s: %s' % (item.find('term').text, item.find('definition').text)


top = sys.argv[1]

assert os.path.exists(top)

for dirpath, dnames, fnames in os.walk(top):
    for f in fnames:
        doc_file = os.path.join(dirpath, f)
        doc = parse(doc_file)
        root = doc.getroot()

        if root.tag == 'course-standard':
            import_course_standard(root)
        elif root.tag == 'tf-questions':
            import_tf_questions(root)
        elif root.tag == 'glossary-items':
            import_glossary_items(root)
        else:
            assert False
        print

