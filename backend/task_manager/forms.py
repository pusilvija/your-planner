from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'status', 'category', 'description', 'order']

    # Ensure the fields are not required
    name = forms.CharField(required=False)
    status = forms.CharField(required=False)
    category = forms.CharField(required=False)
    description = forms.CharField(required=False, widget=forms.Textarea)

    order = forms.IntegerField(widget=forms.HiddenInput(), required=False)
