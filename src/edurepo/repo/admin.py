from django.contrib import admin

from repo.models import Course, LearningObjective, GlossaryItem, TrueFalseItem

admin.site.register(Course)
admin.site.register(LearningObjective)
admin.site.register(GlossaryItem)
admin.site.register(TrueFalseItem)
