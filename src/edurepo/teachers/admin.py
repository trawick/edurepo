from django.contrib import admin

from teachers.models import Teacher, TeacherClass, Entry

admin.site.register(Teacher)
admin.site.register(TeacherClass)
admin.site.register(Entry)
