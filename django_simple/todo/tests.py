import json

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
