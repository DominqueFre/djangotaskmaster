from datetime import date

from django.test import TestCase

from .forms import TaskForm
from .models import Category


class TaskFormTests(TestCase):
	def test_form_is_valid_with_required_fields(self):
		form = TaskForm(data={'title': 'Submit report', 'due_date': date(2026, 3, 20)})
		self.assertTrue(form.is_valid())

	def test_form_is_valid_with_category(self):
		category = Category.objects.create(name='Admin')
		form = TaskForm(
			data={
				'title': 'Send invoice',
				'due_date': date(2026, 3, 22),
				'category': category.id,
			}
		)
		self.assertTrue(form.is_valid())

	def test_form_is_invalid_without_title(self):
		form = TaskForm(data={'due_date': date(2026, 3, 20)})
		self.assertFalse(form.is_valid())
		self.assertIn('title', form.errors)

	def test_form_is_invalid_without_due_date(self):
		form = TaskForm(data={'title': 'Missing date'})
		self.assertFalse(form.is_valid())
		self.assertIn('due_date', form.errors)

	def test_form_widgets_have_expected_css_classes(self):
		form = TaskForm()
		self.assertEqual(form.fields['title'].widget.attrs.get('class'), 'form-control')
		self.assertEqual(form.fields['due_date'].widget.attrs.get('class'), 'form-control')
		self.assertEqual(form.fields['category'].widget.attrs.get('class'), 'form-select')
