from django.contrib import admin

from teachers.models import Teacher, Course, Entry

admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Entry)
