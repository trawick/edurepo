from django import forms
from models import Resource


class ResourceForm(forms.ModelForm):

    objective = forms.CharField(label="Learning objective")
    url = forms.CharField(label="URL of resource")

    class Meta:
        model = Resource
        fields = ('objective', 'url', 'notes')