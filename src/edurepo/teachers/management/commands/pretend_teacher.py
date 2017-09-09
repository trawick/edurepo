import datetime
import json
import sys

from django.contrib.auth.models import User
import djclick as click

from teachers.models import Entry, Teacher, TeacherClass


def create_pretend_teacher(base_api_url, noisy=True):
    teacher_data = ('ms.teacher@example.edu', 'testuser', 'Ms. Teacher', 'AL-G5-SCIENCE', '5th grade science',
                    ['AL-G5-SCIENCE-05A', 'AL-G5-SCIENCE-05A', 'AL-G5-SCIENCE-05B', 'AL-G5-SCIENCE-05D',
                     'AL-G5-SCIENCE-05D'])
    users = User.objects.filter(username=teacher_data[1])
    if users:
        u = users[0]
    else:
        if noisy:
            print '%s does not exist, creating...' % teacher_data[1]
        u = User.objects.create_user(teacher_data[1], email=teacher_data[0])
    Teacher.objects.filter(email=teacher_data[0]).delete()
    t = Teacher(email=teacher_data[0], user=u, name=teacher_data[2])
    t.save()
    c = TeacherClass(teacher=t, course_id=teacher_data[3], name=teacher_data[4],
                     repo_provider=base_api_url)
    c.save()

    today = datetime.date.today()
    cur_day = today - datetime.timedelta(days=today.weekday())
    for objective in teacher_data[5]:
        e = Entry(teacher=t, teacher_class=c, date=cur_day, objective=objective)
        e.save()
        cur_day += datetime.timedelta(days=1)


@click.command()
@click.option('--from-json', type=click.File('r'),
              help='name of file with JSON-formatted base API URL')
@click.argument('base_api_url', type=str, default=None, required=False)
def main(from_json, base_api_url):
    if bool(from_json) == bool(base_api_url):
        click.echo('Either JSON file or API URL is required')
        sys.exit(1)

    if from_json:
        url = json.load(from_json)['base_api_url']
        from_json.close()
    else:
        url = base_api_url
    create_pretend_teacher(url)
