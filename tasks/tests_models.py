from datetime import date

from django.test import TestCase

from .models import Category, Task


class CategoryModelTests(TestCase):
	def test_category_string_representation_returns_name(self):
		category = Category.objects.create(name='Work')
		self.assertEqual(str(category), 'Work')


class TaskModelTests(TestCase):
	def test_task_string_representation_returns_title(self):
		task = Task.objects.create(title='Pay bills', due_date=date(2026, 3, 10))
		self.assertEqual(str(task), 'Pay bills')

	def test_task_defaults_to_not_completed(self):
		task = Task.objects.create(title='Book appointment', due_date=date(2026, 3, 12))
		self.assertFalse(task.completed)

	def test_task_can_be_created_without_category(self):
		task = Task.objects.create(title='Gym session', due_date=date(2026, 3, 15))
		self.assertIsNone(task.category)
