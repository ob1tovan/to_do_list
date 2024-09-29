from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'complete', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Task title <3'}),
            'description': forms.Textarea(attrs={
                'style': 'resize:none; width:100%; height:150px;',
                'placeholder': 'Enter task description...',
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'style': 'border: 1px solid #ccc; border-radius: 5px; padding: 10px;',
            })
        }