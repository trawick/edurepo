from django import forms
from django.utils.translation import gettext as _
from models import Teacher


class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ('email', 'name')
        labels = {'email': _('E-mail for students to contact you')}
