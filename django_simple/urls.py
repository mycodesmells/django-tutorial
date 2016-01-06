from django.conf.urls import include, url
from django.contrib import admin

from django_simple.authentication import urls as authentication_urls 
from django_simple.todo import urls as todo_urls 


urlpatterns = [
	url(r'^', include(todo_urls)),
	url(r'^', include(authentication_urls)),

    url(r'^admin/', include(admin.site.urls)),
]
