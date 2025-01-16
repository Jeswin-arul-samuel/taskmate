from django.shortcuts import render, redirect
from todolist_app.models import TaskList
from .form import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# Create your views here.
@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manager = request.user
            instance.save()
            current_page = request.GET.get('current_page',1)
        messages.success(request, ("New Task Added!"))
        current_page = request.GET.get('current_page',1)
        return HttpResponseRedirect(f'?page={current_page}')
    else:
        all_tasks = TaskList.objects.filter(manager=request.user)
        paginator = Paginator(all_tasks, 7) #show 7 tasks per page
        page = request.GET.get('page')
        all_tasks = paginator.get_page(page)
        return render(request, 'todolist.html', {'all_tasks': all_tasks})

@login_required   
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task.delete()
        messages.success(request, ("Task Deleted!"))
    else:
        messages.error(request, ("Access Restricted, You are not allowed to delete this task!"))
    return redirect('todolist')

@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
        messages.success(request, ("Task Updated!"))
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task_obj': task_obj})

@login_required    
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, ("Access Restricted, You are not allowed to mark this task as complete!"))
    return redirect('todolist')

@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task.done = False
        task.save()
    else:
        messages.error(request, ("Access Restricted, You are not allowed to mark this task as pending!"))
    return redirect('todolist')

def index(request):
    context = {'index_text':'Homepage',
               
               }
    return render(request, 'index.html', context)


def contact(request):
    context = {'contact_text':'Contact Us',
               
               }
    return render(request, 'contact.html', context)

def about(request):
    context = {'about_text':'About Us',
               
               }
    return render(request, 'about.html', context)