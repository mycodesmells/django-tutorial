from django.conf.urls import include, url
from django.contrib import admin

from . import views


urlpatterns = [
	url(r'^$', views.index),
	url(r'^add/$', views.add),
	url(r'^delete/(?P<task_id>\d+)/$', views.delete),

	url(r'^api/tasks/$', views.TasksApiView.as_view(), name='tasks_api_view'),
	url(r'^api/tasks/(?P<task_id>\d+)/$', views.delete_task),
]
