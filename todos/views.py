from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Task


def index(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if title:
            Task.objects.create(title=title)
        return redirect('todos:index')

    tasks = Task.objects.all()
    return render(request, 'todos/index.html', {'tasks': tasks})


@require_POST
def toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.done = not task.done
    task.save(update_fields=['done'])
    return redirect('todos:index')


@require_POST
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('todos:index')
