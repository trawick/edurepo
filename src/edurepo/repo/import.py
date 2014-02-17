import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'edurepo.settings')

import sys
sys.path.append('.')

from xml.etree.ElementTree import parse


from repo.models import Course, LearningObjective, GlossaryItem, TrueFalseItem

perform_import = False
noisy = False


def import_course_standard(root):
    id = root.get('id')
    description = root.find('description').text

    if perform_import:
        c = Course(id=id, description=description)
        c.save()

    if noisy:
        print 'Course standard: %s' % id
        print description

    # don't care about <source></source> for now

    objectives = root.find('objectives')

    for child in objectives:
        id = child.get('id')
        description = child.find('description').text

        if noisy:
            print 'Objective: %s' % id
            print '  %s' % description

        if perform_import:
            c.learningobjective_set.create(id=id, formal_description=description)


def import_tf_questions(root):
    for obj_group in root.findall('objective-group'):
        obj_id = obj_group.find('objective-id').text

        if noisy:
            print 'T-F questions for objective %s:' % obj_id

        if perform_import:
            obj = LearningObjective.objects.get(id=obj_id)

        for question in obj_group.findall('question'):
            stmt = question.find('statement').text
            ans  = True if question.find('answer').text == 'T' else False

            if noisy:
                print '  %s (%s)' % (stmt, ans)

            if perform_import:
                obj.truefalseitem_set.create(statement=stmt, answer=ans)


def import_glossary_items(root):
    for obj_group in root.findall('objective-group'):
        obj_id = obj_group.find('objective-id').text

        if noisy:
            print 'Glossary items for objective %s:' % obj_id

        if perform_import:
            obj = LearningObjective.objects.get(id=obj_id)

        for item in obj_group.findall('item'):
            term = item.find('term').text
            definition = item.find('definition').text

            if noisy:
                print '  %s: %s' % (term, definition)

            if perform_import:
                obj.glossaryitem_set.create(term=term, definition=definition)

if len(sys.argv) != 3:
    print >> sys.stderr, "Usage: %s filesystem-root check-or-import" % sys.argv[0]
    sys.exit(1)

top = sys.argv[1]

mode = sys.argv[2]
assert os.path.exists(top)
assert mode == 'check' or mode == 'import'
if mode == 'import':
    perform_import = True
elif mode == 'check':
    noisy = True

if perform_import:
    # drop existing data before we add the current
    TrueFalseItem.objects.all().delete()
    GlossaryItem.objects.all().delete()
    LearningObjective.objects.all().delete()
    Course.objects.all().delete()

for dirpath, dnames, fnames in os.walk(top):
    for f in sorted(fnames, key=lambda fn: fn[:-4]):
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

        if noisy:
            print

