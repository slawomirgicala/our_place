from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import FlatCreationForm, EnterFlatCreationForm, ChoreCreationForm, AnnouncementCreationForm, TodoForm
from django.contrib import messages
from .models import Flat, Chore, Announcement, Todo
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.utils import timezone


# Create your views here.


@login_required
def home(request):
    # if request.user.is_authenticated():

    if request.user.profile.active_flat is None:
        return redirect('new-flat')
    else:
        todo_list = Todo.objects.filter(flat=request.user.profile.active_flat).order_by('id') #filter by active flat

        form = TodoForm()

        context = {
            'profiles': request.user.profile.active_flat.profiles.all(),
            'todo_list': todo_list,
            'form': form
        }
        return render(request, 'flat/home.html', context)


#    else:
#        return redirect('login')


def about(request):
    return render(request, 'flat/about.html')


@login_required
def new_flat(request):
    if request.method == 'POST':
        form = FlatCreationForm(request.POST)
        if form.is_valid():
            flat = form.save()
            profile = request.user.profile
            profile.flats.add(flat)
            profile.active_flat = flat
            profile.save()
            messages.success(request, f'You have created a new flat!')
            return redirect('flat-home')  # strona glowna mieszkania

    else:
        form = FlatCreationForm()
    return render(request, 'flat/new_flat.html', {'form': form})


@login_required
def enter_flat(request):
    if request.method == 'POST':
        form = EnterFlatCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            try:
                flat = Flat.objects.get(name=name)
            except ObjectDoesNotExist:
                messages.error(request, f'No such flat!')
                return redirect('enter-flat')  # strona glowna mieszkania

            if flat.password != password:
                messages.error(request, f'Wrong password!')
                return redirect('enter-flat')  # strona glowna mieszkania
            else:
                profile = request.user.profile
                profile.flats.add(flat)
                profile.active_flat = flat
                profile.save()
                messages.success(request, f'You entered a flat!')
                return redirect('flat-home')  # strona glowna mieszkania
    else:
        form = FlatCreationForm()
    return render(request, 'flat/enter_flat.html', {'form': form})


@login_required
def new_chore(request):
    if request.method == 'POST':
        form = ChoreCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            flat = request.user.profile.active_flat
            period = form.cleaned_data['period']
            Chore(name=name, flat=flat, period=period, last_made=timezone.now()).save()
            messages.success(request, f'Added new chore :c')
            return redirect('chores-list')
    else:
        form = ChoreCreationForm()
    return render(request, 'flat/new_chore.html', {'form': form})


@login_required
def chores_list(request):
    if request.user.profile.active_flat is None:
        return redirect('new-flat')
    else:
        context = {
            'chores': request.user.profile.active_flat.chore_set.all()
        }
        return render(request, 'flat/chores_list.html', context)


@login_required
def announcements(request):
    if request.user.profile.active_flat is None:
        return redirect('new-flat')
    else:
        context = {
            'announcements': request.user.profile.active_flat.announcement_set.all()
        }
        return render(request, 'flat/announcements.html', context)


@login_required
def new_announcement(request):
    if request.user.profile.active_flat is None:
        return redirect('new-flat')
    else:
        if request.method == 'POST':
            form = AnnouncementCreationForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data['text']
                flat = request.user.profile.active_flat
                user = request.user
                Announcement(text=text, flat=flat, user=user).save()
                messages.success(request, f'succesfully announced')
                return redirect('flat-announcements')  # lita obowiazkow
        else:
            form = AnnouncementCreationForm()
    return render(request, 'flat/new_announcement.html', {'form': form})


@require_POST
def addTodo(request):
    form = TodoForm(request.POST)

    if form.is_valid():
        new_todo = Todo(text=request.POST['text'])
        new_todo.flat = request.user.profile.active_flat
        new_todo.save()

    return redirect(home)


def completeTodo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.complete = True
    todo.save()

    return redirect(home)


def deleteCompleted(request):
    Todo.objects.filter(complete__exact=True, flat=request.user.profile.active_flat).delete()

    return redirect(home)

