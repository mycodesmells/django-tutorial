# Django Tutorial - Writing tests for REST views

We've already taken a look on writing some tests for models, but how about views? After all, they are one of the most important pieces of Django puzzle. In this post we take a look on how to test REST API views, which return some data or statuses. 

### Types of Django views

We can distinguish two types of Django views - those that render HTML templates and those that are so called data _endpoints_. The latter are often used in APIs that can be reached for example via your Java Script requests which allow you to create Single Page Applications. You just ask for data, and then refresh just a part of your page.

So how we test Django views? We do not really test those HTML-rendering ones, as it does not make sense if you think about it. When it comes to API views, you absolutely need to make tests for those. But how exactly do we do this? 

### Writing tests

Let's take a look on our API view first:

	def get(self, request, *args, **kwargs):
		tasks = Task.objects.all()
		json = [model_to_dict(t) for t in tasks]
		return JsonResponse(json, safe=False)

So what tests should we create? I can think of three:

- should return an empty JSON array when there are no `Task` model instances,
- should return a sigle-element JSON array when there is only one `Task`,
- should return a multiple-element JSON array when there are more

We start by creating a class in our `test.py` file within the _todo_ app:

	class ViewsTests(TestCase):

	def test_should_return_empty_array(self):
		pass

	def test_should_return_one_element_array(self):
		pass

	def test_should_return_multi_element_array(self):
		pass

In order to do those tests correctly we need to do follow a popular _given-when-then_ test writing rule:

- **given** that the database stores given data,
- **when** we perform the HTTP request,
- **then** we receive expected result

The trick for writing view tests is to use `RequestFactory` to produce a `request` parameter for your views. It comes with some cool methods, so that your request have various data (such as URL, method type, etc) injected automatically. So our query test for empty array begins like this:

	...
	from django.test import RequestFactory, TestCase
	...

	def test_should_return_empty_array(self):
		# given
		factory = RequestFactory()

		# when
		request = factory.get('/api/tasks/')
		result = views.TasksApiView().get(request)

		# then

Notice that we don not do anything with database in _given_ section. But we already have some instances in our production database, is there a problem? Not at all! When running tests, Django is actually creating a brand new test database, to ensure that its state is the same every time we run. We want to test the case when there is nothing in the database, so we do not need to juggle anything.

Now how do we check the result? We definitely have to! It's not so easy to do, Or maybe it's easy, but requires a few lines of code. First we need to extract content from the response and decode it to UTF-8 string (as it is stored as byte array):

	# then
	str_content = result.content.decode("utf-8")

then, for covenient assertions later, we load this string to a dictionary, that looks just like the JSON we got:

	...
	import json
	...
	json_content = json.loads(str_content)

With this object we can finally check the contents:

	self.assertEqual(len(json_content), 0)

The result of running our tests should look like this:

	$ ./manage.py test django_simple.todo.tests.ViewsTests
	Creating test database for alias 'default'...
	.
	----------------------------------------------------------------------
	Ran 1 test in 0.002s

	OK
	Destroying test database for alias 'default'...


### Access restrictions

The last problem we need to address, is restricting the access to our API views. We do not want to allow anybody to query the data, do we? If our view has some user-authenticated-only access decorator, our test will fail:

	$ ./manage.py test django_simple.todo.tests.ViewsTests
	Creating test database for alias 'default'...
	E
	======================================================================
	ERROR: test_should_return_empty_array (django_simple.todo.tests.ViewsTests)
	...
	AttributeError: 'WSGIRequest' object has no attribute 'user'

	...
	FAILED (errors=1)
	Destroying test database for alias 'default'...
	
As you can see, the error trace actually gives us a hint about what is missing in our test. Django is looking for a `request.user` property, which is injected automatically when some authenticated user is requesting the view. The only thing we need to do is add the property manually:

	...
	from django.contrib.auth.models import User
	...
		def test_should_return_empty_array(self):
			...
			u1 = User.objects.create(username="u1")
			...
			request.user = u1
			...

Now when we call the tests, it's perfect:

	$ ./manage.py test django_simple.todo.tests.ViewsTests
	Creating test database for alias 'default'...
	.
	----------------------------------------------------------------------
	Ran 1 test in 0.003s

	OK
	Destroying test database for alias 'default'...

**Note: ** Restricting access to a class-view does not take a `@login_required` decorator, but `@method_decorator(login_required)`:

	...
	from django.utils.decorators import method_decorator
	...
	class TasksApiView(View):
		@method_decorator(login_required)
		def get(self, request, *args, **kwargs):
			...

		@method_decorator(login_required)
		def post(self, request, *args, **kwargs):
			...

### Extracting common test start

As you can see looking at our tests cases, there are some things that would happen every time. In this case, we can share those using a `setUp()` function. The only thing we need to remember, is that if you need to pass some paramter into a specific test case function, you need to do it via `self.your_important_object` class attribute. In our case, the `setUp()` should contain:

	...
	def setUp(self):	import json

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from . import models, views

class TaskTests(TestCase):

	def test_should_return_name_with_x_as_undone_task_str_representation(self):
		t = models.Task(name='some name', done=False)
		self.assertEqual(str(t), "[✖] some name")

	def test_should_return_name_with_x_as_done_task_str_representation(self):
		t = models.Task(name='some name', done=True)
		self.assertEqual(str(t), "[✔] some name")

def response_to_json(response):
	str_content = response.content.decode("utf-8")
	return json.loads(str_content)

class ViewsTests(TestCase):

	def setUp(self):
		self.user = User.objects.create(username="u1")
		self.factory = RequestFactory()

	def test_should_return_empty_array(self):
		# when
		request = self.factory.get('/api/tasks/')
		request.user = self.user
		response = views.TasksApiView().get(request)
		json_content = response_to_json(response)

		# then
		self.assertEqual(len(json_content), 0)

	def test_should_return_one_element_array(self):
		# given
		models.Task.objects.create(name='only task')

		# when
		request = self.factory.get('/api/tasks/')
		request.user = self.user
		response = views.TasksApiView().get(request)
		json_content = response_to_json(response)

		# then
		self.assertEqual(len(json_content), 1)

	def test_should_return_multi_element_array(self):
		# given
		models.Task.objects.create(name='task #1')
		models.Task.objects.create(name='task #2', done=True)
		models.Task.objects.create(name='task #3')

		# when
		request = self.factory.get('/api/tasks/')
		request.user = self.user
		response = views.TasksApiView().get(request)
		json_content = response_to_json(response)

		# then
		self.assertEqual(len(json_content), 3)

		self.user = User.objects.create(username="u1")
		self.factory = RequestFactory()
	...

That way we can reuse those objects later on:

	def test_should_return_empty_array(self):
		...
		request = self.factory.get('/api/tasks/')
		request.user = self.user
		...

Now if you think about it, we don't need a **given** part any more, as we have that code executed in `setUp` function.

### Final result

Our `test.py` file (without models tests) should look like this:

	import json

	from django.contrib.auth.models import User
	from django.test import RequestFactory, TestCase

	from . import models, views

	... # models tests

	class ViewsTests(TestCase):

		def setUp(self):
			self.user = User.objects.create(username="u1")
			self.factory = RequestFactory()

		def test_should_return_empty_array(self):
			# when
			request = self.factory.get('/api/tasks/')
			request.user = self.user
			response = views.TasksApiView().get(request)
			json_content = response_to_json(response)

			# then
			self.assertEqual(len(json_content), 0)

		def test_should_return_one_element_array(self):
			# given
			models.Task.objects.create(name='only task')

			# when
			request = self.factory.get('/api/tasks/')
			request.user = self.user
			response = views.TasksApiView().get(request)
			json_content = response_to_json(response)

			# then
			self.assertEqual(len(json_content), 1)

		def test_should_return_multi_element_array(self):
			# given
			models.Task.objects.create(name='task #1')
			models.Task.objects.create(name='task #2', done=True)
			models.Task.objects.create(name='task #3')

			# when
			request = self.factory.get('/api/tasks/')
			request.user = self.user
			response = views.TasksApiView().get(request)
			json_content = response_to_json(response)

			# then
			self.assertEqual(len(json_content), 3)

**Note** that when we execute saves in tests, we have our post-save actions executed, so don't be surprised to see something besides test executions status in your logs!

You can check out a full source code [on Github](https://github.com/mycodesmells/django-tutorial).
