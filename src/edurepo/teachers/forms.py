from django import forms
from django.utils.translation import gettext as _
from models import Teacher, TeacherClass


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
