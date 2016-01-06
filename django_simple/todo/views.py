from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import TaskForm
from .models import Task


@login_required
def index(request):
	tasks = Task.objects.all()

	return render(request, "index.html", {
			'tasks': tasks
		})

@login_required
def add(request):
	if request.method == 'POST':
		form = TaskForm(request.POST)

		if form.is_valid():
			name = form.cleaned_data["name"]

			task = Task(name=name)
			task.save()

	return redirect('/')

@login_required
def delete(request, task_id):
	Task.objects.get(id=task_id).delete()
	return redirect('/')