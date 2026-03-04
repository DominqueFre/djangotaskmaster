from datetime import date

from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Task


TEST_STORAGES = {
	'default': {
		'BACKEND': 'django.core.files.storage.FileSystemStorage',
	},
	'staticfiles': {
		'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
	},
}


@override_settings(STORAGES=TEST_STORAGES)
class IndexViewTests(TestCase):
	def test_index_get_returns_success_and_template(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'index.html')

	def test_index_post_creates_task_and_redirects(self):
		response = self.client.post(
			reverse('index'),
			data={'title': 'Create from form', 'due_date': date(2026, 3, 25)},
		)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse('index'))
		self.assertTrue(Task.objects.filter(title='Create from form').exists())


@override_settings(STORAGES=TEST_STORAGES)
class TaskActionViewTests(TestCase):
	def setUp(self):
		self.task = Task.objects.create(title='Action task', due_date=date(2026, 3, 30), completed=False)

	def test_delete_task_post_deletes_task(self):
		response = self.client.post(reverse('delete_task', args=[self.task.id]))
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse('index'))
		self.assertFalse(Task.objects.filter(id=self.task.id).exists())

	def test_toggle_complete_post_sets_true_when_checkbox_on(self):
		response = self.client.post(reverse('toggle_complete', args=[self.task.id]), data={'completed': 'on'})
		self.assertEqual(response.status_code, 302)
		self.task.refresh_from_db()
		self.assertTrue(self.task.completed)

	def test_toggle_complete_post_sets_false_when_checkbox_absent(self):
		self.task.completed = True
		self.task.save(update_fields=['completed'])

		response = self.client.post(reverse('toggle_complete', args=[self.task.id]))
		self.assertEqual(response.status_code, 302)
		self.task.refresh_from_db()
		self.assertFalse(self.task.completed)
