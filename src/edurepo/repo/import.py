import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'edurepo.settings')

import sys
sys.path.append('.')

from xml.etree.ElementTree import parse


from repo.models import Course, CourseCategory, LearningObjective, ICan, \
    GlossaryItem, MultipleChoiceItem, ReferenceText, TrueFalseItem

perform_import = False
noisy = False


def import_course_categories(root):
    categories = root.findall('category')
    for category in categories:
        category_id = category.get('id')
        description = category.find('description').text

        if perform_import:
            cat = CourseCategory(id=category_id, description=description)
            cat.save()


def import_course_standard(root):
    course_id = root.get('id')
    description = root.find('description').text

    # Blow up if the category is not declared.
    cat = root.find('category')
    assert cat is not None, 'Course category is not defined for course %s' % course_id
    cat_id = root.find('category').text

    try:
        # Blow up if the category id is not known.
        cat = CourseCategory.objects.get(id=cat_id)
    except CourseCategory.DoesNotExist:
        if perform_import:
            assert False, 'Category %s is not valid (course %s).' % (cat_id, course_id)
        else:
            print "Warning: Category %s is unknown" % cat_id

    if perform_import:
        c = Course(id=course_id, cat=cat, description=description)
        c.save()
    else:
        c = None

    if noisy:
        print 'Course standard: %s' % course_id
        print '                 %s' % description
        print

    # don't care about <source></source> for now

    objectives = root.find('objectives')

    for child in objectives:
        objective_id = child.get('id')
        description = child.find('description').text

        if noisy:
            print 'Objective: %s' % objective_id
            print '           %s' % description.encode('utf-8')

        if perform_import:
            c.learningobjective_set.create(id=objective_id, description=description)

        icans = child.find('icans')
        if icans is not None:
            for ican in icans:
                if noisy:
                    print '  ICan: ' + ican.text

                if perform_import:
                    obj = LearningObjective.objects.get(id=objective_id)
                    obj.ican_set.create(statement=ican.text)

        reference = child.find('reference')
        if reference is not None:
            if noisy:
                print '  Reference: ' + reference.text

            if perform_import:
                obj = LearningObjective.objects.get(id=objective_id)
                obj.referencetext_set.create(text=reference.text)


def import_tf_questions(root):
    for obj_group in root.findall('objective-group'):
        obj_id = obj_group.find('objective-id').text

        if noisy:
            print 'T-F questions for objective %s:' % obj_id

        if perform_import:
            obj = LearningObjective.objects.get(id=obj_id)
        else:
            obj = None

        for question in obj_group.findall('question'):
            stmt = question.find('statement').text
            ans = True if question.find('answer').text == 'T' else False

            if noisy:
                print '  %s (%s)' % (stmt, ans)

            if perform_import:
                obj.truefalseitem_set.create(statement=stmt, answer=ans)


def import_mc_questions(root):
    for obj_group in root.findall('objective-group'):
        obj_id = obj_group.find('objective-id').text

        if noisy:
            print 'Multiple choice questions for objective %s:' % obj_id

        if perform_import:
            obj = LearningObjective.objects.get(id=obj_id)
        else:
            obj = None

        for mc_question in obj_group.findall('mc-question'):
            question = mc_question.find('question').text
            choice1 = mc_question.find('choice1').text
            choice2 = mc_question.find('choice2').text
            choice3 = mc_question.find('choice3')
            if choice3 is not None:
                choice3 = choice3.text
            choice4 = mc_question.find('choice4')
            if choice4:
                choice4 = choice4.text
            choice5 = mc_question.find('choice5')
            if choice5:
                choice5 = choice5.text
            q_type = mc_question.find('type').text
            answer = mc_question.find('answer').text

            if noisy:
                print '  %s/%s/%s/%s/%s/%s/%s/%s' % (question, choice1, choice2, choice3, choice4, choice5, q_type,
                                                     answer)

            if perform_import:
                kw = dict()
                kw['question'] = question
                kw['choice1'] = choice1
                kw['choice2'] = choice2
                if choice3:
                    kw['choice3'] = choice3
                if choice4:
                    kw['choice4'] = choice4
                if choice5:
                    kw['choice5'] = choice5
                kw['type'] = q_type
                kw['ans'] = int(answer)

                obj.multiplechoiceitem_set.create(**kw)


def import_glossary_items(root):
    for obj_group in root.findall('objective-group'):
        obj_id = obj_group.find('objective-id').text

        if noisy:
            print 'Glossary items for objective %s:' % obj_id

        if perform_import:
            obj = LearningObjective.objects.get(id=obj_id)
        else:
            obj = None

        for item in obj_group.findall('item'):
            term = item.find('term').text
            definition = item.find('definition').text

            if noisy:
                print '  %s: %s' % (term, definition)

            if perform_import:
                obj.glossaryitem_set.create(term=term, definition=definition)


def go(top):
    if perform_import:
        # drop existing data before we add the current
        TrueFalseItem.objects.all().delete()
        GlossaryItem.objects.all().delete()
        LearningObjective.objects.all().delete()
        Course.objects.all().delete()
        CourseCategory.objects.all().delete()
        ICan.objects.all().delete()
        MultipleChoiceItem.objects.all().delete()
        ReferenceText.objects.all().delete()

    for dirpath, _, fnames in os.walk(top):
        for f in sorted(fnames, key=lambda fn: fn[:-4]):
            doc_file = os.path.join(dirpath, f)
            doc = parse(doc_file)
            root = doc.getroot()

            if root.tag == 'course-categories':
                import_course_categories(root)
            elif root.tag == 'course-standard':
                import_course_standard(root)
            elif root.tag == 'tf-questions':
                import_tf_questions(root)
            elif root.tag == 'mc-questions':
                import_mc_questions(root)
            elif root.tag == 'glossary-items':
                import_glossary_items(root)
            else:
                assert False, 'Document tag "%s" is not recognized.' % root.tag

            if noisy:
                print

if len(sys.argv) != 3:
    print >> sys.stderr, "Usage: %s filesystem-root check-or-import" % sys.argv[0]
    sys.exit(1)

x_top = sys.argv[1]

x_mode = sys.argv[2]
assert os.path.exists(x_top)
assert x_mode == 'check' or x_mode == 'import'
if x_mode == 'import':
    perform_import = True
elif x_mode == 'check':
    noisy = True

go(x_top)
