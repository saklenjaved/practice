from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

# Create your views here.

def index(request):
    tasks = Task.objects.all().order_by('-created')
    
    if request.method == 'GET':
        form = TaskForm()
        return render(request, 'index.html', {'tasks': tasks, 'form': form})
    
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'index.html', {'form': form, 'tasks': tasks})
    
def update_task(request, task_id):
    task = Task.objects.get(id=task_id)
    
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'update.html', {'form': form})
    
    elif request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'update.html', {'form': form})
    
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('/')