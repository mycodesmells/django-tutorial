# Django Tutorial - Basic Authentication

Django tutorial: 
[Part 1](http://mycodesmells.com/post/django-tutorial-virtualenv/) [Part 2](http://mycodesmells.com/post/django-tutorial-the-most-basic-project/) [Part 3](http://mycodesmells.com/post/django-tutorial-editing-data/)

Have you ever created a web application that did not require your users to log in? Me neither, because sooner or later there comes a time that it just needs to be done. There are may reasons behind this: your system might be working with some critical data, you want to determine who made some change to the data or just want to restrict access to some data sets for some users. So, without further ado, let's take a look on the simplest way you can implement login/logout functionality in our Django application.

### Restricting views access

You might want to start with creating login and logout page, but we are taking a completely different approach here. First, we want to restrict the access to our views so that nobody can access them unless they are authenticated. You might want to add some validation code to a view, such as:

	def index(request):
		if not request.user.is_authenticated():
        	return redirect('/login')

		# actual request handling

Although this works perfectly fine, there is one major flaw here: you need to copy-paste it to each view (which is tedious but we could cope with that), and if you ever want to change anything, eg. the redirection destination, it would create a massive amount of work. Fortunately, there is much clearner way to do this, via **decorator** called `login_required`:

	@login_required
	def index(request):
		# actual request handling

Let's take a look on what happens now, when we start the application and go to the root page.

<img src="https://raw.githubusercontent.com/mycodesmells/django-tutorial/master/posts/images/login-required-default.png"/>

Now that is strange, because we have been redirected to `/accounts/login/?next=/`. At least we were successfully denied access to the page. Let's say that we don't want to create our login pages under `/accounts` path, but directly on `/login`? This can be changed in our project settings, just add:

	# rest of the settings
	
	LOGIN_URL = '/login/'

Before we go any further, let's reorganize our URL dispatcher configuration, so that we will have the base URLs in separate file from those responsible for authentication. But we start with creating a new Django app in `django_simple/authentication` (note, that we cannot use `auth` as there is already core application with this name). Then let's split those `urls.py`:

	# django_simple/todo/urls.py
	...
	from . import views

	urlpatterns = [
		url(r'^$', views.index),
		url(r'^add/$', views.add),
		url(r'^delete/(?P<task_id>\d+)/$', views.delete),
	]

and incude them, as well as newly created ones in the root `urls.py`:

	# django_simple/urls.py
	...
	from django_simple.authentication import urls as authentication_urls 
	from django_simple.todo import urls as todo_urls 

	urlpatterns = [
		url(r'^', include(todo_urls)),
		url(r'^', include(authentication_urls)),

	    url(r'^admin/', include(admin.site.urls)),
	]	

### Using built-in auth views

The simplest way you can create authentication views is by using those provided by Django. All you need to do is pass them in appropriate urls file:

	# django_simple/authentication/urls.py
	...
	urlpatterns = [
		url(r'^login/$', 'django.contrib.auth.views.login'),
		url(r'^logout/$', 'django.contrib.auth.views.logout'),
	]

Now accessing the root page results in:

<img src="https://raw.githubusercontent.com/mycodesmells/django-tutorial/master/posts/images/login-page-missing-template.png"/>

What is that? Oh, right, Django knows to render login page here, but does not quite knows how the page should look like. You can see, that it is lookig for a teplate file `authentication/templates/registration/login.html`. Let's create it, then!

	{% if form.errors %}
		<p>Invalid credentials</p>
	{% endif %}

	<form method="post" action="{% url 'django.contrib.auth.views.login' %}">
	{% csrf_token %}
	<table>
	<tr>
	    <td>{{ form.username.label_tag }}</td>
	    <td>{{ form.username }}</td>
	</tr>
	<tr>
	    <td>{{ form.password.label_tag }}</td>
	    <td>{{ form.password }}</td>
	</tr>
	</table>

	<input type="submit" value="login" />
	<input type="hidden" name="next" value="{{ next }}" />
	</form>

What happens now? You can see, that we are using some mysterious `form` object here - it is injected into the template by django login view, so that you don't need to worry about the inputs. So we finally have our login form, but it just doesn't look very good. Now, when we have two templates in use in our app (`login.html` and `index.html`), it might be a good time to create some base template with page header for example, to make it look prettier:

	<!-- django_simple/todo/templates/base.html -->
	<!DOCTYPE html>
	<html>
	<head>
		...
	</head>
	<body>

	<div class="col-sm-6 col-sm-offset-3">
		<div class="page-header">
		  <h1>Too Doo <small>a django application example</small></h1>
		</div>

		{% block content %}
		{% endblock %}
	</div>
	...

We can now remove the header from `index.html` and put all the content into the `content` block:

	{% extends "base.html" %}

	{% block content %}
		<ul class="list-group">
			...		
		</ul>
	{% endblock %}

Our login page should look similar - just put the login form into the block as well:

	{% extends "base.html" %}

	{% block content %}

	{% if form.errors %}
		<p>Invalid credentials</p>
	{% endif %}
	<form>
	...
	</form>

	{% endblock %}

Now it looks much better:

<img src="https://raw.githubusercontent.com/mycodesmells/django-tutorial/master/posts/images/login-page-from-template.png"/>

How about logging out? Adding some information about currently logged in user with, plus logout link should be a good idea:

**base.html**:

	<div class="page-header">
		...
		<div class="user-name">
		  	{% if not user.is_anonymous %}
		  		<strong>Logged as:&nbsp;</strong> {{user}} &nbsp;
				<a href="/logout" title="Log out"><span class="fa fa-sign-out"></span></a>
			{% endif %}
		</div>
	</div>

As you can see, there is another object injected automatically into the template, that is `user`. Now we should see the username and a pretty logout button. Clicking on it leads us to the default Django logout page (actually logout confirmation page). The problem is, that this page is connected to Django admin panel, and clicking on _Log in again_ link actually leads us to the admin panel login, instead of our application's.

To fix this, we should get rid of the default Django logout view and create a simple one, that will end user's session and redirect to the application root:

	def logout_view(request):
	    logout(request)
	    return redirect('/')

and add change it in the `authentication/urls.py`:

	...
	urlpatterns = [
		url(r'^login/$', 'django.contrib.auth.views.login'),
	    url(r'^logout/$', views.logout_view),
	]

Does it work now? Awww, it does!
