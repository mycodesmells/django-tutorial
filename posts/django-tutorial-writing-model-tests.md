# Django Tutorial - Writing model tests

We have already developed a few functionalities, but still haven't managed to write any tests. That might seem unnecessary at this point, but in fact we should not keep it this way any longer. The sooner you start writing tests for your code, the sooner it is natural for you and you'll be more sure that the latest commit does not break anything. Let's delve into Django tests then!

When developing a Django application, you generally have two types of tests you want to write: **model tests** and **view tests**. The first group represent all things you instantiate during a test case, validate its internal state and that's it. The second one is slightly more complicated, as it involves calling a view method that takes some HTTP request and return specific response data.

### Not only model tests

In fact, limiting those tests to just models is not entirely correct. You might find yourself creating some _helper_ classes, that are not represented by any database model, but still require some tests. For example, you might have a object/function that will count the number of created tasks since the last login. It might look like this:

	def tasks_since_last_login(tasks, user):
		...

As you can see, this might not be placed in any model, so that it's, let say, _detached_ from `models.py`. Anyway, if you want to tests it, you would do it just as with any model tests: create an user and a list of tasks, set some date as user's last login and check if the number of tasks returned by the function is correct.

### First test

So how do we write a test then? We begin with creating a `tests.py` file in our app's folder (in our case `django_simple/todo/tests.py`). I would like to check if `__str__()` method generates a correct string representation of my Task. Let's create a simple test case that creates a Task:

	from django.test import TestCase

	from .models import Task

	class TaskTests(TestCase):

		def test_should_return_name_with_x_as_undone_task_str_representation(self):
			t = Task(name='some name', done=False)
			print(t)

It this it? You probably noticed that we are missing somethin, that is actual validation if the result is correct. Let's say that we want our task's name to be prepended with "[✔]" or "[✖]" depending on their `done` status. We can run our current tests with a command:

	$ ./manage.py test
	Creating test database for alias 'default'...
	some name
	.
	----------------------------------------------------------------------
	Ran 1 test in 0.000s

	OK
	Destroying test database for alias 'default'...

### Defining expectations

As you can see, we printed our task's `__str__()` value and it's not what we want, but the test passed. How do we change this? We need to tell Django what do we expect:

	...
	def test_should_return_name_with_x_as_undone_task_str_representation(self):
		t = Task(name='some name', done=False)
		self.assertEqual(str(t), "[✖] some name")
	...

Now when we run this test, it will react properly:

	(venv)slomek@slomek-mint /opt/workspace/mycodesmells/django-tutorial $ ./manage.py test
	Creating test database for alias 'default'...
	F
	======================================================================
	FAIL: test_should_return_name_as_str_representation (django_simple.todo.tests.TaskTests)
	----------------------------------------------------------------------
	Traceback (most recent call last):
	  File "/opt/workspace/mycodesmells/django-tutorial/django_simple/todo/tests.py", line 9, in test_should_return_name_as_str_representation
	    self.assertEqual(str(t), "[✖] some name")
	AssertionError: 'some name' != '[✖] some name'
	- some name
	+ [✖] some name
	? ++++


	----------------------------------------------------------------------
	Ran 1 test in 0.001s

	FAILED (failures=1)
	Destroying test database for alias 'default'...

Once we change the `__str__()` method:

	def __str__(self):
        if self.done:
            return "[✔] %s" % self.name
        else:
            return "[✖] %s" % self.name

and add one more test (for done tasks and _check_ sign as a prefix), we should see the success test result:

	$ ./manage.py test
	Creating test database for alias 'default'...
	..
	----------------------------------------------------------------------
	Ran 2 tests in 0.001s

	OK
	Destroying test database for alias 'default'...


In the next post I will shortly describe how do we write view tests, mainly for API endpoints.
