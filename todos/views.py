from django.shortcuts import render, redirect
from .models import Task, Category
from .forms import TaskForm, CategoryForm

# Create your views here.

def index(request):
    todo = Task.objects.select_related('category').all().order_by('-created_at')
    categories = Category.objects.all()
    
    return render(request, 'index.html', {'todo': todo, 'categories': categories})

def update_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'GET':
        form = CategoryForm(instance=category)
        return render(request, 'update_category.html', {'category': category, 'form': form})
    elif request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, 'update_category.html', {'category': category, 'form': form})
    
def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect('index')

def todo_by_category(request, category_id):
    todo = Task.objects.filter(category_id=category_id)
    category = Category.objects.get(id=category_id)    
    return render(request, 'todo_by_category.html', {'todo': todo, 'category': category})

def done_tasks(request):
    todo = Task.objects.filter(done=True)
    
    return render(request, 'index.html', {'todo': todo, 'message': "All Done Tasks"})

def update_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'update_task.html', {'form': form, 'task': task})
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
        return redirect(request, 'update_task.html', {'form': form, 'task': task})
    
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('/')
