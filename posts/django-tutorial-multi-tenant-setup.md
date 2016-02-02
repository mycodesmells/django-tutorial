# Django Tutorial - Multi Tenant Setup

Recently in a project I'm invoved in, we faced a situation in which we wanted to split the application among several clients in a way, that the data is accessed separately for each of them. On top of that, we wanted to give each client a separate access to the application. Now we could have created appropriate endpoints, or make the user send the client information with each and every request... Fortunately there is a better way - multi-tenant environment. This post allows you to replicate this setup in your own project, step by step.

The most important aspect of multi-tenancy is separating data and its access. The first thing that a user notices when entering such environment, is a specific subdomain via which the app is accessed, such as `client1.app.com`, `client2.app.com` etc. This seems to be a large piece of work, but in fact it is pretty easy to do, especially in Django. 

### django-tenant-schemas

If you ever want to create a multi-tenant application using Django, you should try out _django-tenant-schemas_ library. It's very easy to set up and use, and despite having some drawbacks, it really is a good choice.

As we are going to have our database separated between subdomains, we need to use some database engine that enables that. Postgres is  a very popular choice, and it is supported natively by _django-tenant-schemas_. If you don't want to install it on your machine, you can go with docker image. The only thing you are going to need is a development package for the DB:

	sudo apt-get install postgresql-server-dev-9.4

### Database setup

Pull docker image and put it into a directory where you will create your `docker-endpoint.sh` script that will create your database and users. You can copy it from an official repository, or from mine.

	$ cd postgres-docker/
	$ docker run -ti -e POSTGRES_PASSWORD=todo -e POSTGRES_USER=todo -e POSTGRES_DB=todo -d postgres

One thing that we'll need is an IP address of our docker container:

	$ docker ps
	CONTAINER ID        IMAGE		...
	9583463fa82d        postgres	...

	$ docker inspect awesome_wing | grep IPAddress
	...
        "IPAddress": "172.17.0.2",
    ...

### Application setup

First we need to install the package:

	$ pip install django-tenant-schemas
	...
	Successfully installed django-tenant-schemas psycopg2
	Cleaning up...

As you noticed, that last command installs `psycopg2` package as well, which is a driver for our database. Then we can pretty much follow [the manual](https://django-tenant-schemas.readthedocs.org/en/latest/).

First, we should create an app that is going to store information about our tenants:

	django-admin.py startapp tenants
	
**Note:** We need to create this app in a top-level directory (where we keep eg. `manage.py` file). Then create a model responsible for that:

	from django.db import models
	from tenant_schemas.models import TenantMixin

	class Tenant(TenantMixin):
	    name = models.CharField(max_length=100)
	    
	    auto_create_schema = True

As you can see, it is very simple (just the name), but there are some fields inherited from `TenantMixin` superclass. What is important is `auto_create_schema = True` setting, which causes Django to run database schema migrations after creating an instance. I can't think of a reason not to enable that.

Now when we have the Tenant model, we can edit the most important part, `settings.py` file. First we need to decide which apps will have their data shared between tenants, and which should be separated. In our case, we'll share authentication (by default `django-tenant-schemas` shares users and it's a bit tricky to change it), but split `todo` - we would like to see two separate _To Do_ lists. We do all this using `SHARED_APPS` and `TENANT_APPS` settings:


	SHARED_APPS = (
	    'tenant_schemas',
	    'tenants',
	    'django_simple.authentication',
	    'django.contrib.contenttypes',
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	)
	TENANT_APPS = (
	    # The following Django contrib apps must be in TENANT_APPS
	    'django.contrib.contenttypes',
	    'django_simple.todo',
	)
	INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

Then we need to add middleware and template processor:

	MIDDLEWARE_CLASSES = (
		'tenant_schemas.middleware.TenantMiddleware',
	...
	TEMPLATES = [
         'APP_DIRS': True,
         'OPTIONS': {
             'context_processors': [
             	'django.core.context_processors.request',
 	...

OK, but how our application will know where to look for tenant definitions. It won't, unless we define it:

	TENANT_MODEL = "tenants.Tenant"

Last, but not least, we need to change our database settings to use our Postgres on Docker:

	DATABASES = {
	     'default': {
	        'ENGINE': 'tenant_schemas.postgresql_backend',
	        'NAME': 'todo',
	        'USER': 'todo',
	        'PASSWORD': 'todo',
	        'HOST': '172.17.0.2',
	        'PORT': '5432'
	    }
	}
	DATABASE_ROUTERS = (
	    'tenant_schemas.routers.TenantSyncRouter',
	)

We should be good to go now, just run the database migrations (notice that it's different from the original `migrate`) and create superuser, so that we can log in:

	$ ./manage.py makemigrations
	Migrations for 'tenants':
	  0001_initial.py:
	    - Create model Tenant

	$ ./manage.py migrate_schemas --shared
	...

	$ ./manage.py createsuperuser
	Enter Tenant Schema ('?' to list schemas): ?
	public - toodoo.com
	first - first.toodoo.com
	second - second.toodoo.com
	Enter Tenant Schema ('?' to list schemas): first
	Username (leave blank to use 'slomek'): admin
	Email address: admin@admin.admin
	Password: 
	Password (again): 

	$ ./manage.py runserver

**Note:** Even though `createsuperuser` script asks for a tenant to create the user on, it is shared between all tenants.

But wait, which tenant should we access? That's the point. At this stage we don't have any, so that we need to create at least one. Let's do it via Django's shell.

First we need to create a _public_ tenant, which will be accessible when no subdomain is selected.

	$ ./manage.py shell
	>>> from tenants.models import Tenant
	>>> t = Tenant(domain_url='toodoo.com',schema_name='public',name='public')
	>>> t.save()

Notice that nothing extraordinary happenned after save. But watch what happens when you try to create another tenant, this time running on a subdomain:

	>>> t2 = Tenant(domain_url='first.toodoo.com',schema_name='first',name='First')
	>>> t2.save()
	=== Running migrate for schema first
	Operations to perform:
	  Apply all migrations: auth, admin, sessions, tenants, todo, contenttypes
	Running migrations:
	  Rendering model states... DONE
	  Applying contenttypes.0001_initial... OK
	  Applying auth.0001_initial... OK
	  Applying admin.0001_initial... OK
	  Applying admin.0002_logentry_remove_auto_add... OK
	  Applying contenttypes.0002_remove_content_type_name... OK
	  Applying auth.0002_alter_permission_name_max_length... OK
	  Applying auth.0003_alter_user_email_max_length... OK
	  Applying auth.0004_alter_user_username_opts... OK
	  Applying auth.0005_alter_user_last_login_null... OK
	  Applying auth.0006_require_contenttypes_0002... OK
	  Applying auth.0007_alter_validators_add_error_messages... OK
	  Applying sessions.0001_initial... OK
	  Applying tenants.0001_initial... OK
	  Applying todo.0001_initial... OK
	>>> t3 = Tenant(domain_url='second.toodoo.com',schema_name='second',name='Second')
	>>> t3.save()
	...
	  Applying todo.0001_initial... OK

Remember the setting for auto-running migrations after creating a `Tenant` instance. That was it!

Is it all? Can we access it already? Nope! The very last thing we need to do is change our `/etc/hosts` file, so that entering our domain addresses redirects us to our localhost

	...
	127.0.0.1	toodoo.com first.toodoo.com second.toodoo.com
	...

### Final result

First, let's run the server, enter `first.toodoo.com` and create a task:

	$ ./manage.py runserver

<img src="https://raw.githubusercontent.com/mycodesmells/django-tutorial/multi-tenancy/posts/images/first-tenant.png"/>

You can see that the task exists. What happens when we switch to `second.toodoo.com`?

<img src="https://raw.githubusercontent.com/mycodesmells/django-tutorial/multi-tenancy/posts/images/second-tenant.png"/>

Yep, the task is nowhere to be found. Success!

The source code of this example is available [on Github](https://github.com/mycodesmells/django-tutorial), on branch `multi-tenancy`.
