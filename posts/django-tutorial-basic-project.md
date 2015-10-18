# Django Tutorial - The Most Basic Project

Django tutorial: Part 1

It's time to make the first step in actually developing our first project in Django. In this post we will create a simple module which will be responsible for managing our To Do list. At the end of this piece we will have a semi-pretty which will list our tasks, and we'll get to know a little bit about django's administration panel. Let's dive in!

### Setting up the project

First, let's start by enabling our Python Virtual Environment (see previous Part 1 in this series). Then we'd have to install django and start our little project:

	$ pip instal django
	$ django-admin.py startproject django_simple

It will create a simple, raw structure of django project. In order to proceed, we need to create a module within the project, which in django's case is called an app. But first, we need to make our first architectural decision here: do we create all of our apps on the top level (i.e. the same as our `manage.py` file), or do we prefer to nest them inside our `django_simple` folder. I prefer the latter, for two reasons. First, it shows that our apps are the part of the root app. The second argument is particularily important if you are building a project with a thick client side. If so, you can divide your project into two directories: one will keep all django code, and the second all JS/CSS?/HTML code build with some separate tool. This makes the code much easier to be managed during development.

	$ cd django_simple/
	$ django-admin.py startapp todo

### Django background

Creating a simple application in django is almost extremely easy. The most powerful aspect of the framework is its famous administration panel which can be used for doing any database modifications. Maybe its design is not quite modern (it's ugly as hell in my opinion) but the functionality is awesome! On top of that, django is configured to use SQLite database by default, which really speeds up the development process, especially at the beginning. Keeping your database in a separate file makes it easy to check out something and quickly backup your data before trying to make any potentially breaking changes. To see your empty project up and running you need to do just a few simple things via your command line:

	$ ./manage.py migrate
	$ ./manage.py createsuperuser
	$ ./manage.py runserver
	Performing system checks...

	System check identified no issues (0 silenced).
	October 18, 2015 - 21:39:53
	Django version 1.8.5, using settings 'django_simple.settings'
	Starting development server at http://127.0.0.1:8000/
	Quit the server with CONTROL-C.

First command initializes your database (creates tables, inserts initial required data), second is theoretically optional (but is necessary for administration panel access) and allows you to create your super user (administator with all privileges). Finally, the last one starts a server and allows you to access it via your web browser.

### Creating a model

To make anything custom in your django application, you need to start with a model. It is a representation of a database entity (and, consequently, table). Class and field definition is very easy, thanks to `django.db.models` module, which offers base class and field types. In our case, we'll be creating a simpe Task model which keeps only two pieces of information: task's name and whether it has been already done or not. We will also add one method to the class, `__str__`, which is responsible for displaying Task instance as a String value whenever we would like to print it to console, or, as you will see later, to display it in administration panel in a readable format.

**models.py**:

	from django.db import models

	class Task(models.Model):
		name = models.TextField(max_length=100)
		done = models.BooleanField(default=False)

		def __str__(self):
			if self.done:
				return "%s (done)" % self.name
			else:
				return self.name

### Administration panel

Actually, adding a model is not quite enough to see it in the administration panel. You need to manually define the entities you enable to be edited via the panel, which may come in handy if you prefer to hide some information. To use django's default admin view for a model, all you need to define is to create **admin.py** file wich this content:

	from django.contrib import admin
	from .models import Task

	admin.site.register(Task)

### Views and templates

We have the model, we can edit it, but now we need to display it somehow. To do this we need two things: a view and a template. A view is a method defined and build in Python, that takes a HTTP request object and returns a HTTP response with some data handled by a browser. In our case, we'll create one simple view that will read all tasks from the database, and render a template based on that data:

**views.py**:

	from django.shortcuts import render
	from .models import Task

	def index(request):
		tasks = Task.objects.all()

		return render(request, "index.html", {
				'tasks': tasks
			})

There are three important things to note here. First, that our model, _Task_ comes with a useful ORM tool (called a Manager) that makes it so easy to make any queries to the database. In this case, we want to get all tasks, so we call `Task.objects.all()`, which returns a list of all database entries. Second thing is a `render` method that takes two required parameters: HTTP request and templates name. The third one is optional, as you can create a template that does not use any context data. We will be showing a list of tasks, so we need a context object with this data.

Last but not least, we need to craete a HTML template, in which we can benefit from django's template language. We can iterate through the tasks list and display specific items using traditional HTML tags. We will be using three basic template features: for-loop, if-else and value rendering.


**templates/index.html**:
	
	<!DOCTYPE html>
	<html>
	<!-- ... -->
	<div class="col-sm-6 col-sm-offset-3">
		
		<div class="page-header">
		  <h1>Too Doo <small>a django application example</small></h1>
		</div>

		<ul class="list-group">

			{% for task in tasks %}
				<li class="list-group-item task-item">
				  	<div class="col-xs-1">
			  			{% if task.done %}
				  			<span class="fa fa-check-square-o"></span>
						{% else %}
				  			<span class="fa fa-square-o"></span>
						{% endif %}

				  	</div>
					<div class="col-xs-11">{{ task.name }}</div>
				</li>		
			{% endfor %}		
		</ul>

	</div>

	</body>
	</html>

### Adding to the project

Whenever we make any changes to the database structure: changing models, adding new ones of deleting some, we need to prepare information about those changes. This way, if we share the project with somebody else, they know what they need to do with their database to keep it combatible with the code. To do that we need to execute two commands:

	$ ./manage.py makemigrations
		Migrations for 'todo':
		  0001_initial.py:
	$ ./manage.py migrate

Next, we need to inform django, which routes should be directed to our view functions, so that we can access appopriate template:

**urls.py**:

	from django.conf.urls import include, url
	from django.contrib import admin

	from django_simple.todo import views as todo_views


	urlpatterns = [
		url(r'^$', todo_views.index),

	    url(r'^admin/', include(admin.site.urls)),
	]

After doing that we actually have our app ready to run. To make it look better, we'll use some Bootstrap features, so that appropriate CSS files need to be references in our HTML template. After that we can run our application and see the results:

	
This is not quite what we want to see. But we can enter our administration panel (running on http://localhost:8000/admin), click on Task link and add some items. Let's add (_Add task_ button on the right) one task marked as done, and one yet to be finished:

Now when we refresh the root page, we can see the list with two cool items!

### To do

This application is clearly not finished yet. We have to edit the database items via administration panel, instead of the page in a browser. In the next part of the tutorial we'll create some views and forms to enable all these operations.