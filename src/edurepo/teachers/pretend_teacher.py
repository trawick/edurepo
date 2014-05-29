import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'edurepo.settings')

import sys
sys.path.append('.')

import datetime
from django.contrib.auth.models import User
from teachers.models import Entry, Teacher, TeacherClass


def process():
    teacher_data = ('ms.teacher@example.edu', 'testuser', 'Ms. Teacher', 'AL-G5-SCIENCE', '5th grade science',
                    ['AL-G5-SCIENCE-05A', 'AL-G5-SCIENCE-05A', 'AL-G5-SCIENCE-05B', 'AL-G5-SCIENCE-05D',
                     'AL-G5-SCIENCE-05D'])
    users = User.objects.filter(username=teacher_data[1])
    if users:
        u = users[0]
    else:
        print '%s does not exist, creating...' % teacher_data[1]
        u = User.objects.create_user(teacher_data[1], email=teacher_data[0])
    Teacher.objects.filter(email=teacher_data[0]).delete()
    t = Teacher(email=teacher_data[0], user=u, name=teacher_data[2])
    t.save()
    c = TeacherClass(teacher=t, course_id=teacher_data[3], name=teacher_data[4])
    c.save()

    today = datetime.date.today()
    cur_day = today - datetime.timedelta(days=today.weekday())
    for objective in teacher_data[5]:
        e = Entry(teacher=t, teacher_class=c, date=cur_day, objective=objective)
        e.save()
        cur_day += datetime.timedelta(days=1)

process()
