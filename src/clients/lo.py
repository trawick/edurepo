from datetime import datetime, timedelta
import json
import urllib2

# http://127.0.0.1:8000/teachers/api/entry/?format=json&teacher__email=trawick@gmail.com&date__lte=2014-02-16&date__gte=2014-02-09
base_teacher_url = 'http://127.0.0.1:8000/teachers/api/entry/'
teacher_email = 'trawick@gmail.com'
teacher_class = 'MG4'

# fetch learning objects for the past week for the specified teacher

today_dt = datetime.now()
week_ago_dt = today_dt - timedelta(days=7)

today = today_dt.strftime('%Y-%m-%d')
week_ago = week_ago_dt.strftime('%Y-%m-%d')

url = '%s?format=json&teacher__email=%s&date__lte=%s&date__gte=%s&course__name=%s' % (base_teacher_url, teacher_email, today, week_ago, teacher_class)
response = urllib2.urlopen(url)
body = response.read()
jbody = json.loads(body)
objs = jbody['objects']
for obj in objs:
    print '%s: %s' % (obj['date'], obj['objective'])
    # now fetch description of this objective
