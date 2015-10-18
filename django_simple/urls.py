from django.conf.urls import include, url
from django.contrib import admin

from django_simple.todo import views as todo_views


urlpatterns = [
	url(r'^$', todo_views.index),

    url(r'^admin/', include(admin.site.urls)),
]
