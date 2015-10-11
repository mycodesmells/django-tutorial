from django import forms

class TaskForm(forms.Form):
    name = forms.CharField(max_length=100)