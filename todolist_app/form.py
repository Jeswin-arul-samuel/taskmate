from django import forms
from .models import TaskList

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['task', 'done']  # This will display the task and done fields in the form.