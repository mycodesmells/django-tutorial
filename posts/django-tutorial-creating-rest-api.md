# Django Tutorial - Creating REST APIs

In the [previous post](http://mycodesmells.com/post/django-tutorial-writing-model-tests/) we took a look on how to write simple Django tests for models (and any helper functions). This time we are going to work with view tests, that are returning something. In this post we will build a simple REST API that can later be tested with view tests.

### Endpoints basics

In our simple project we will implement three REST views:

	GET		/api/tasks
	POST	/api/tasks
	DELETE	/api/tasks/<id>

Their implementation of `/api/tasks` should look like this:

	...
	from django.http import JsonResponse
	...

	def get_all_tasks(request):
		tasks = Task.objects.all()
		return JsonResponse(tasks)

It looks simple enough, but actually it does not work. After putting this view in one of the `urls.py` files an accessing the URL, we will find out that

	In order to allow non-dict objects to be serialized set the safe parameter to False

Fine, let's update the last line of our view then:

	...
	return JsonResponse(tasks, safe=False)
	...

Does it work already? No? Why not this time? It turns out, that our array is not serializable. In order to go around this problem we can use Django forms' utility function called `model_to_dict`. The only problem with this approach is that we cannot call it on the whole query set, but individually. We can use a clever one-line mapper to achieve that quite elegantly:

	...
	from django.forms import model_to_dict
	...
	def get_all_tasks(request):
		tasks = Task.objects.all()
		json = [model_to_dict(t) for t in tasks]
		return JsonResponse(json, safe=False)

Now if we call the endpoint it finally returns (newlines added for better readability):

	[{"name": "first task", "id": 1, "done": true}, 
	{"name": "second task", "id": 2, "done": false}, 
	{"name": "third task", "id": 3, "done": true}]	

### Custom response codes

In order to follow the whole idea of a REST API, you need to realize that not only the data returned is important, but also the HTTP response code. It is essential for POST and DELETE calls, as it determines if the query was successful. For example, when posting a new item via REST, we expect to receive the newly created object's ID and status code 201 (_Created_):

	...
	from django.views.decorators.http import require_POST
	...

	@require_POST
	def post_item(request):
		name = request.POST.get("name", "")
		done = request.POST.get("1", "0") is not "0"
		task = Task.objects.create(name=name, done=done)
		task.save()
		return HttpResponse(task.id, status=201)

The problem is, that we now have two views (`get_all_tasks` and `post_item`) on the same URL, but using different HTTP method types. The solution is to introduce a class view. It involves three steps:

- move your views into `TasksApiView` class that extends django.views.generic.View,
- rename your views to `get` and `post`
- change your `urls.py` entry to `url(r'^api/tasks/$', views.TasksApiView.as_view(), name='tasks_api_view'),`

Now we need to test our POST view which is a bit trickier, as we need to juggle a bit of JavaScripts. If you thought about jQuery, you need to check out [You Might Not Need JQuery](http://youmightnotneedjquery.com/) page and execute this code in your browser's console:

	// get cookie value by name
	function getCookie(name) {
	    var value = '; ' + document.cookie;
	    var parts = value.split(`; ${name}=`);
	    if (parts.length === 2) {
	        return parts.pop().split(';').shift();
	    }
	}


	var request = new XMLHttpRequest();
	request.open('POST', '/api/tasks/', true);
	request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
	request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	request.send("name=another task, added via POST");

After a second or so, we can check the result:

	console.info("Return code:", request.status);
	> Return code: 201
	console.info("Newly created ID:", request.responseText");
	> Newly created ID: 4

### Delete view

This view should be the easiest one, as we have it ona a separate URL, we have a simple logic inside. The only thing we need to focus on here is to introduce a dynamic URL parameter to determine which item should be deleted. The view itself looks like this:

	def delete_task(request, task_id):
		Task.objects.get(id=task_id).delete()
		return HttpResponse(status = 204)

Now in order to inject `task_id` parameter into the view, we need to create a dynamic URL entry in `urls.py`:

	url(r'^api/tasks/(?P<task_id>\d+)/$', views.delete_task),

Now you can call it:

	function getCookie(name) {
	    var value = '; ' + document.cookie;
	    var parts = value.split(`; ${name}=`);
	    if (parts.length === 2) {
	        return parts.pop().split(';').shift();
	    }
	}


	var request = new XMLHttpRequest();
	request.open('DELETE', '/api/tasks/4', true);
	request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
	request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	request.send("name=another task, added via POST");

	...

	console.info("Return code:", request.status);
	> Return code: 204

You can now enjoy your pretty REST API! You can view the code [on Github](https://github.com/mycodesmells/django-tutorial).
