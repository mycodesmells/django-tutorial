# Django Tutorial - Editing Data

Django tutorial: [Part 1](http://mycodesmells.com/post/django-tutorial-virtualenv/) [Part 2](http://mycodesmells.com/post/django-tutorial-the-most-basic-project/)

Since we've already covered the basics of Django's models and template-rendering view, it's time to introduce some data manipulations accessible to the end users. We'll create our first form and a couple of views for saving and editing to-do items.

### Creating a Django form

Whenever there is a need for submitting some data to Django's backend, you can make use of the framework's built-in elements - forms. The idea is really simple: you create an HTML form and a Python class that is a back-end representation of it. This way you can easily perform some actions on it, such as data validation.

We'll start with creating an HTML form. We'll insert it into our existing `index.html` template:

**index.html**:

	<li class="list-group-item new-task-item task-item">
	  	<form action="/add" method="post">
	  		{% csrf_token %}
			<div class="col-xs-1 form-group">
			</div>
			<div class="col-xs-10 form-group">
				<input class="form-control" name="name" placeholder="Enter task name...">
			</div>
			<div class="col-xs-1 form-group">
				<button type="submit" class="btn btn-link">
	  				<span class="fa fa-check save-button"></span>
				</button>					
			</div>
		</form>
	</li>

You might notice a strange template element within the form - `{% csrf_token %}`. This is a part of Django's policy for Cross Site Request Forgery Protection (read more in [the docs](https://docs.djangoproject.com/en/1.8/ref/csrf/)). 

The second, aformentioned element, is a form class. Traditionally it should be placed in `forms.py` file within out todo application. As you can see in the HTML part, we will have only one field for our to-do item - it name. By default, our new item will be set as not done yet (it wouldn't make much sense to save finished tasks), that's why our form will be as simple as this:

**forms.py**:

	from django import forms

	class TaskForm(forms.Form):
	    name = forms.CharField(max_length=100)

### Add item view

The last thing we need to complete our process of adding tasks is a view which will make actual changes to the database and update a list in the browser. Our idea is to check if the form data is correct, add the Task item and redirect our request to the main page which will show updated list.

**views.py**:

	def add(request):
		if request.method == 'POST':
			form = TaskForm(request.POST)

			if form.is_valid():
				name = form.cleaned_data["name"]

				task = Task(name=name)
				task.save()

		return redirect('/')

As you can see, we start by checking if a view is accessed with POST request method. We don't want to have GET requests update data, do we? Once we know that the method type is correct, we actually want to validate form's data. Here's where Django's forms' default `is_valid()` method comes in handy. If the data is truely correct, we ca proceed to executing database modifications. And agan, our Task item is as easy as any model can be. Once we save a model instance, we can redirect user to the page.

### Deleting items

It would not be fair for our users, if we just allow them to add tasks without a possibility to delete them. As we still don't have a backend logic for changing Task's statuses between _finished_ and _not finished_, this will be their only way to mock this expected behaviour. 

First, we need to create a view that will delete a Task item from database and will redirect us the main page, just as with `add` view:

**views.py**:

	def delete(request, task_id):
		Task.objects.get(id=task_id).delete()
		return redirect('/')

There is nothing too complicated here - we find a Task item with given ID, and delete it. The most important thing is happenning in URLs definitions file:

**urls.py**:

	...
	url(r'^add$', todo_views.add),
	url(r'^delete/(?P<task_id>\d+)$', todo_views.delete),
	...

Right below defining our `add` view (which is a simple non-argument view), we need to create one for deleting item. This one is a bit trickier, as we need to read a Task's ID from request's URL and pass it into the view. To do this we use `(?P<task_id>\d+)` which can be translated into _get a number and keep it as task_id variable_. Remember to have `\d+`, as the plus sign is very important at the end - this way we require at last one digit, while still allowing more. Having `\d` would end in a single-digit-only queries, while `\d*` would allow us to make this request with empty ID, which should not be supported.

Last, but not least, we need to update our view, so that there is a way to delete an item from our page's UI:

	{% for task in tasks %}
		<li class="list-group-item task-item">
		  	<div class="col-xs-1">
	  			{% if task.done %}
		  			<span class="fa fa-check-square-o"></span>
				{% else %}
		  			<span class="fa fa-square-o"></span>
				{% endif %}

		  	</div>
			<div class="col-xs-10">{{ task.name }}</div>
		  	<div class="col-xs-1 actions-column">
		  		<a href="/delete/{{task.id}}"><span class="fa fa-times"></span></a>
		  	</div>
		</li>		
	{% endfor %}

You can see that we've added a simple link element in each data row, which will trigger our delete view (with correct Task's ID).

### To do

With our next tutoral part, we would need to allow users to mark tasks as finished or not, without the need to deleting them.