from datetime import datetime, timedelta
import json
import urllib2
import sys

if len(sys.argv) != 3:
    print >> sys.stderr, "Usage: %s teacher-email class-name" % sys.argv[0]
    sys.exit(1)

teacher_email = sys.argv[1]
teacher_class = sys.argv[2]

course_name = teacher_class  # pretend these are the same for now

server_base = 'http://127.0.0.1:8000/'
base_teacher_url = '%steachers/api/entry/' % server_base
base_course_url = '%srepo/api/course/' % server_base
base_objective_url = '%srepo/api/learningobjective/' % server_base

# fetch learning objects for the past week for the specified teacher

today_dt = datetime.now()
week_ago_dt = today_dt - timedelta(days=7)

today = today_dt.strftime('%Y-%m-%d')
week_ago = week_ago_dt.strftime('%Y-%m-%d')

url = '%s?format=json&teacher__email=%s&date__lte=%s&date__gte=%s&course__name=%s' % \
      (base_teacher_url, teacher_email, today, week_ago, teacher_class)
response = urllib2.urlopen(url)
body = response.read()
json_body = json.loads(body)
objs = json_body['objects']

if len(objs) == 0:
    print >> sys.stderr, "No learning objectives were found."
    # Todo: Try to retrieve classes for this teacher to see if the teacher
    #       e-mail is wrong or if the class is wrong.
    sys.exit(1)

url = '%s%s?format=json' % (base_course_url, course_name)
response = urllib2.urlopen(url)
body = response.read()
json_body = json.loads(body)
course_description = json_body['description']

print 'Current objectives for %s:' % course_description

for obj in objs:
    print '  %s: %s' % (obj['date'], obj['objective'])
    # now fetch description of this objective
    url = '%s%s?format=json' % (base_objective_url, obj['objective'])
    response = urllib2.urlopen(url)
    body = response.read()
    json_body = json.loads(body)
    print '    %s' % (json_body['formal_description'])
