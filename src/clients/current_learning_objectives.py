from datetime import datetime, timedelta
import json
import urllib, urllib2
import sys

if len(sys.argv) != 4:
    print >> sys.stderr, "Usage: %s base-url teacher-email class-name" % sys.argv[0]
    sys.exit(1)

teacher_email = sys.argv[2]
teacher_class = sys.argv[3]

if sys.argv[1] == 'dev':
    server_base = 'http://127.0.0.1:8000/'
elif sys.argv[1] == 'prod':
    server_base = 'http://edjective.org/ed/'
else:
    server_base = sys.argv[1]

base_teacher_url = '%steachers/api/entry/' % server_base
base_course_url = '%srepo/api/course/' % server_base
base_objective_url = '%srepo/api/learningobjective/' % server_base

# fetch learning objects for the past week for the specified teacher

today_dt = datetime.now()
week_ago_dt = today_dt - timedelta(days=7)

today = today_dt.strftime('%Y-%m-%d')
week_ago = week_ago_dt.strftime('%Y-%m-%d')

url = '%s?format=json&teacher__email=%s&date__lte=%s&date__gte=%s&teacher_class__name=%s' % \
      (base_teacher_url, teacher_email, today, week_ago, urllib.quote(teacher_class))
response = urllib2.urlopen(url)
body = response.read()
json_body = json.loads(body)
objs = json_body['objects']

if len(objs) == 0:
    print >> sys.stderr, "No learning objectives were found."
    # Todo: Try to retrieve classes for this teacher to see if the teacher
    #       e-mail is wrong or if the class is wrong.
    sys.exit(1)

course_id = objs[0]['teacher_class']['course_id']
url = '%s%s/?format=json' % (base_course_url, course_id)
response = urllib2.urlopen(url)
body = response.read()
json_body = json.loads(body)
course_description = json_body['description']

print 'Current objectives for %s (%s):' % (teacher_class, course_id)
print

for obj in objs:
    print '  %s: %s' % (obj['date'], obj['objective'])
    # now fetch description of this objective
    url = '%s%s/?format=json' % (base_objective_url, obj['objective'])
    response = urllib2.urlopen(url)
    body = response.read()
    json_body = json.loads(body)
    print '    %s' % json_body['description'].strip()
