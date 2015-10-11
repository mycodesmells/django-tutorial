from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

from .forms import TaskForm
from .models import Task


def index(request):
	tasks = Task.objects.all()

	return render(request, "index.html", {
			'tasks': tasks
		})

@csrf_protect
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

# def mark_as_done(request)

# def matk_as_undone(request)