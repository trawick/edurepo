from django.contrib import admin

from repo.models import Course, ICan, LearningObjective, MultipleChoiceItem, GlossaryItem, ReferenceText, TrueFalseItem

admin.site.register(Course)
admin.site.register(LearningObjective)
admin.site.register(ICan)
admin.site.register(GlossaryItem)
admin.site.register(MultipleChoiceItem)
admin.site.register(ReferenceText)
admin.site.register(TrueFalseItem)
