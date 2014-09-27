import datetime

from django.contrib import admin

from teachers.models import Teacher, TeacherClass, Entry

admin.site.register(Teacher)
admin.site.register(TeacherClass)


class ExpiredEntryFilter(admin.SimpleListFilter):
    title = 'Expired?'
    parameter_name = 'expired'

    def lookups(self, request, model_admin):
        return (('yes', 'Entries are in the past'),
                ('no', 'Entries are in the present or future'))

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            today = datetime.date.today()
            return queryset.filter(date__lt=today)
        if self.value() == 'no':
            today = datetime.date.today()
            return queryset.filter(date__gte=today)


class EntryAdmin(admin.ModelAdmin):
    list_filter = (ExpiredEntryFilter,)

admin.site.register(Entry, EntryAdmin)
