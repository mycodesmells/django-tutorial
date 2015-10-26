from django.shortcuts import redirect, render

from .forms import TaskForm
from .models import Task


def index(request):
	tasks = Task.objects.all()

	return render(request, "index.html", {
			'tasks': tasks
		})

def add(request):
	if request.method == 'POST':
		form = TaskForm(request.POST)

		if form.is_valid():
			name = form.cleaned_data["name"]

			task = Task(name=name)
			task.save()

	return redirect('/')

def delete(request, task_id):
	Task.objects.get(id=task_id).delete()
	return redirect('/')