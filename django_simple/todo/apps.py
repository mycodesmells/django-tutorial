from django.apps import AppConfig

class TodoConfig(AppConfig):
    name = 'django_simple.todo'
    verbose_name = "To Do"

    def ready(self):
    	from . import emails