from django.conf.urls import include, url
from django.contrib import admin

from django_simple.todo import views as todo_views


urlpatterns = [
	url(r'^$', todo_views.index),
	url(r'^add$', todo_views.add),
	url(r'^delete/(?P<task_id>\d+)$', todo_views.delete),

    url(r'^admin/', include(admin.site.urls)),
]
