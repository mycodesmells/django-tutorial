from django.conf.urls import include, url
from django.contrib import admin

from . import views


urlpatterns = [
	url(r'^$', views.index),
	url(r'^add/$', views.add),
	url(r'^delete/(?P<task_id>\d+)/$', views.delete),
]
