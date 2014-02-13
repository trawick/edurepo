from django.contrib import admin

from repo.models import Course, LearningObjective, GlossaryItem

admin.site.register(Course)
admin.site.register(LearningObjective)
admin.site.register(GlossaryItem)
