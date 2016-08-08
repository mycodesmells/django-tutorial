# Django Tutorial - Signals

Django tutorial: 
[Part 1](http://mycodesmells.com/post/django-tutorial-virtualenv/) [Part 2](http://mycodesmells.com/post/django-tutorial-the-most-basic-project/) [Part 3](http://mycodesmells.com/post/django-tutorial-editing-data/) [Part 4](http://mycodesmells.com/post/django-tutorial-basic-authentication/)

There is already much going on in our example application. We have user authentication, creating tasks and marking them as complete. But how about performing some actions any time something specific happens? We have two options to go with, let's take a look which is better and when.

### Overriding save method

This is fairly obvious choice, at least it was for me at first. If I want to make something happen whenever I change a model, I should override the default save behaviour and add anything I want. Let's say that we want to log information about any changes made to one of the tasks in our app:

	# django_simple/todo/models.py
	import logging
	from django.db import models
	logger = logging.getLogger(__name__)

	class Task(models.Model):
		# ...

	    def save(self, *args, **kwargs):
	        logger.warning("Task model change (name=%s)" % self.name)
	        super(Task, self).save(*args, **kwargs)

It comes in handy because it gives very easy access to the model's properties, as we were able to get Task's name instantly. Now whenever we save a Task instance, we can see appropriate information in the log:

<img src="https://raw.githubusercontent.com/mycodesmells/django-tutorial/master/posts/images/save-logging.png"/>

### Using post_save signals

Another approach, one I was not familiar with for a long time, is creating a signal handler. This might be useful for some less model-specific actions, such as sending an e-mail whenever a Task instance is saved. The main advantage of this approach is, that you don't need to handle this action in the same place where you keep your model definition. Actually there is nothing you need to do in the `models.py` at all. Let's create another file for fake mailing service:

	# django_simple/todo/emails.py
	from django.db.models.signals import post_save
	from django.dispatch import receiver
	from .models import Task
	...

	@receiver(post_save, sender=Task)
	def send_mail_on_task_save(sender, instance, **kwargs):
	    logger.warning("Sending email as task \"%s\" has been saved." % instance.name)

But that is not all unfortunately. By extracting this code to a separate file, we lost the auto-load of our code into the running Python project (as `models.py` are loaded implicitly). To load this we need to make it manually, with the best choice being the `apps.py` configuration. First create/edit `django_simple/todo/apps.py` file to make it look like this:

	from django.apps import AppConfig

	class TodoConfig(AppConfig):
	    name = 'django_simple.todo'
	    verbose_name = "To Do"

	    def ready(self):
	    	from . import emails

We've defined the app's configuration and want to load our `emails.py` file as soon as it is ready to used in the project. Second step is to inform django about the `apps.py`, which should be done in app's `__init__.py`:

	default_app_config = 'django_simple.todo.apps.TodoConfig'

Now let's save a task and look at the console:

<img src="https://raw.githubusercontent.com/mycodesmells/django-tutorial/master/posts/images/save-signal-logging.png"/>

### When to use which?

My experience says, that `save()` is better when you want to manage something strictly related to the model, such as update some calculated field to keep its value consistent with the rest of attributes. Signals on the other hand, are useful for performing some action that is loosely related with the models and do some really specific action. In my current project, for example, we need to have a InfluxDB database for each customer, so that any time a Customer model is saved, we handle the signal and perform this (not really connected to model) action in a separate place.

I also found a pretty good explanation on this choice given [by Jonny Buchanan](http://stackoverflow.com/a/171703) on StackOverflow.
