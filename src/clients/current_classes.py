from datetime import datetime, timedelta
import json
import urllib2
import sys

if len(sys.argv) != 3:
    print >> sys.stderr, "Usage: %s base-url teacher-email" % sys.argv[0]
    sys.exit(1)

teacher_email = sys.argv[2]

if sys.argv[1] == 'dev':
    server_base = 'http://127.0.0.1:8000/'
elif sys.argv[1] == 'prod':
    server_base = 'http://edjective.org/ed/'
else:
    server_base = sys.argv[1]

base_teacher_url = '%steachers/api/teacher_' % server_base
base_course_url = '%srepo/api/course/' % server_base

url = server_base + 'teachers/api/teacher_class/?format=json&teacher__email=%s' % \
    teacher_email
response = urllib2.urlopen(url)
body = response.read()
json_body = json.loads(body)
objs = json_body['objects']

if len(objs) == 0:
    print >> sys.stderr, "No classes were found."
    sys.exit(1)

for obj in objs:
    print '  %s: %s' % (obj['course_id'], obj['name'])
    url = '%s%s/?format=json' % (base_course_url, obj['course_id'])
    response = urllib2.urlopen(url)
    body = response.read()
    json_body = json.loads(body)
    course_description = json_body['description']
    print '    %s' % course_description
