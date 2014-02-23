from django.contrib import admin

from repo.models import Course, ICan, LearningObjective, GlossaryItem, TrueFalseItem

admin.site.register(Course)
admin.site.register(LearningObjective)
admin.site.register(ICan)
admin.site.register(GlossaryItem)
admin.site.register(TrueFalseItem)
