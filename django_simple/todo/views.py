from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View

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

class TasksApiView(View):

	@method_decorator(login_required)
	def get(self, request, *args, **kwargs):
		tasks = Task.objects.all()
		json = [model_to_dict(t) for t in tasks]
		return JsonResponse(json, safe=False)

	@method_decorator(login_required)
	@csrf_exempt
	def post(self, request, *args, **kwargs):
		print(request.POST)
		name = request.POST.get("name", "")
		done = request.POST.get("1", "0") is not "0"
		task = Task.objects.create(name=name, done=done)
		task.save()
		return HttpResponse(task.id, status=201)

@login_required
def delete_task(request, task_id):
	Task.objects.get(id=task_id).delete()
	return HttpResponse(status = 204)
