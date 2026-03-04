from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ['title', 'due_date', 'category']
		widgets = {
			'due_date': forms.DateInput(attrs={'type': 'date'}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Task title'})
		self.fields['due_date'].widget.attrs.update({'class': 'form-control'})
		self.fields['category'].widget.attrs.update({'class': 'form-select'})
