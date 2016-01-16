from django.test import TestCase

from .models import Task

class TaskTests(TestCase):

	def test_should_return_name_with_x_as_undone_task_str_representation(self):
		t = Task(name='some name', done=False)
		self.assertEqual(str(t), "[✖] some name")

	def test_should_return_name_with_x_as_done_task_str_representation(self):
		t = Task(name='some name', done=True)
		self.assertEqual(str(t), "[✔] some name")
