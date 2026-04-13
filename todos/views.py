from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Category, Task


def _redirect_index(filter_category: str) -> HttpResponseRedirect:
    url = reverse('todos:index')
    if filter_category.isdigit():
        url = f'{url}?category={filter_category}'
    return redirect(url)


def index(request):
    raw_filter = request.GET.get('category', '').strip()
    category_filter = None
    if raw_filter.isdigit():
        category_filter = Category.objects.filter(pk=int(raw_filter)).first()

    categories = Category.objects.all()

    if request.method == 'POST':
        new_name = request.POST.get('category_name', '').strip()
        if new_name:
            Category.objects.get_or_create(name=new_name)
            return _redirect_index(request.POST.get('filter_category', '').strip())

        title = request.POST.get('title', '').strip()
        if title:
            task_category = None
            cat_pk = request.POST.get('category', '').strip()
            if cat_pk.isdigit():
                task_category = Category.objects.filter(pk=int(cat_pk)).first()
            Task.objects.create(title=title, category=task_category)
        return _redirect_index(request.POST.get('filter_category', '').strip())

    tasks = Task.objects.select_related('category').all()
    if category_filter:
        tasks = tasks.filter(category=category_filter)

    return render(
        request,
        'todos/index.html',
        {
            'tasks': tasks,
            'categories': categories,
            'category_filter_id': str(category_filter.pk) if category_filter else '',
        },
    )


@require_POST
def toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.done = not task.done
    task.save(update_fields=['done'])
    return _redirect_index(request.POST.get('filter_category', '').strip())


@require_POST
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return _redirect_index(request.POST.get('filter_category', '').strip())
