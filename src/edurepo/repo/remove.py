import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'edurepo.settings')

import sys
sys.path.append('.')

from repo.models import Course, LearningObjective


def delete_learning_objective(lo, delete):
    print 'Deleting objective %s...' % lo
    if delete:
        lo.delete()
    return 0


def delete_course(course, delete):
    courses = Course.objects.filter(id=course)
    assert courses, "Course %s is not in the system" % course
    print 'Deleting course %s...' % courses[0]
    learning_objectives = LearningObjective.objects.filter(course=courses[0])
    for lo in learning_objectives:
        rc = delete_learning_objective(lo, delete)
        if rc:
            return rc
    if delete:
        courses[0].delete()
    return 0


def process(args):
    if len(args) != 2:
        print >> sys.stderr, "Usage: %s course check-or-delete" % sys.argv[0]
        return 1

    course = args[0]
    mode = args[1]

    assert mode == 'check' or mode == 'delete'

    delete = mode == 'delete'

    return delete_course(course, delete)

sys.exit(process(sys.argv[1:]))
