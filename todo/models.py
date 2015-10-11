from django.db import models

class Task(models.Model):
	name = models.TextField(max_length=100)
	done = models.BooleanField(default=False)

	def __str__(self):
		if self.done:
			return "%s (done)" % self.name
		else:
			return self.name