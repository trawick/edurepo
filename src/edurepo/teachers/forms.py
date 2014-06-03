from django import forms
from django.utils.translation import gettext as _
from models import Entry, Teacher, TeacherClass


class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ('email', 'name')
        labels = {'email': _('E-mail for students to contact you')}


class TeacherClassForm(forms.ModelForm):

    class Meta:
        model = TeacherClass
        fields = ('name', 'course_id', 'repo_provider')
        labels = {'name': _('Class name'),
                  'course_id': _('Course id'),
                  'repo_provider': _('Address of course repository')}


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ('objective', 'comments')


def create_entry_form(objective_list):
    """Dynamically create a form like EntryForm above, which presents a list of
    course-specific objectives in a select box, instead of a Textarea.

    XXX I should have been able to override __init__ on EntryForm to create
    the widget for objective in a similar manner.
    """

    class Meta:
        pass

    widget_list = []
    for o in objective_list:
        widget_list += [(o[0], o[0] + ' - ' + o[1])]
    setattr(Meta, 'model', Entry)
    setattr(Meta, 'fields', ('objective', 'comments'))
    widgets = {'objective': forms.Select(choices=widget_list)}
    setattr(Meta, 'widgets', widgets)
    attributes = {'Meta': Meta}

    name = 'DynamicEntryForm'
    base_classes = (forms.ModelForm,)
    form = type(name, base_classes, attributes)
    return form
