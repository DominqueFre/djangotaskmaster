from datetime import date

from django.shortcuts import get_object_or_404, redirect, render

from .models import Task


def index(request):
	pending_tasks = Task.objects.select_related('category').filter(completed=False).order_by('due_date', 'title')
	completed_tasks = Task.objects.select_related('category').filter(completed=True).order_by('due_date', 'title')
	return render(
		request,
		'index.html',
		{
			'pending_tasks': pending_tasks,
			'completed_tasks': completed_tasks,
			'today': date.today(),
		},
	)


def delete_task(request, task_id):
	if request.method == 'POST':
		task = get_object_or_404(Task, pk=task_id)
		task.delete()
	return redirect('index')


def toggle_complete(request, task_id):
	if request.method == 'POST':
		task = get_object_or_404(Task, pk=task_id)
		task.completed = request.POST.get('completed') == 'on'
		task.save(update_fields=['completed'])
	return redirect('index')
