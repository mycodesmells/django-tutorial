from django.shortcuts import render

from .models import Task


def index(request):
	tasks = Task.objects.all()

	return render(request, "index.html", {
			'tasks': tasks
		})