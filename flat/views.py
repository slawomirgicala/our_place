from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import FlatCreationForm, EnterFlatCreationForm, ChoreCreationForm, AnnouncementCreationForm, TodoForm
from django.contrib import messages
from .models import Flat, Chore, Announcement, Todo, ChoreCounter, SpecificChore
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.utils import timezone
from random import choice
from datetime import datetime, timedelta
from django.db.models import Min


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
                if flat in request.user.profile.flats.all():
                    profile = request.user.profile
                    profile.active_flat = flat
                    profile.save()
                    return redirect('flat-home')
                else:
                    profile = request.user.profile
                    profile.flats.add(flat)
                    profile.active_flat = flat
                    profile.save()
                    chores = flat.chore_set.all()
                    for chore in chores:
                        counters = chore.chorecounter_set
                        min_number = counters.aggregate(Min('number'))['number__min']
                        ChoreCounter(chore=chore, user=request.user, number=min_number).save()
                    messages.success(request, f'You entered a flat!')
                    return redirect('flat-home')  # strona glowna mieszkania
    else:
        form = FlatCreationForm()
    return render(request, 'flat/enter_flat.html', {'form': form})


@login_required
def new_chore(request):
    if request.user.profile.active_flat is not None:
        if request.method == 'POST':
            form = ChoreCreationForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                flat = request.user.profile.active_flat
                period = form.cleaned_data['period']
                chore = Chore(name=name, flat=flat, period=period, last_made=timezone.now())
                chore.save()
                profiles = request.user.profile.active_flat.profiles
                for profile in profiles.iterator():
                    ChoreCounter(chore=chore, user=profile.user).save()
                lucky = choice(profiles.all())
                SpecificChore(user=lucky.user, flat=flat, start=timezone.now(),
                              end=timezone.now()+timedelta(days=period), name=name).save()
                messages.success(request, f'Added new chore :c')
                return redirect('chores-list')
        else:
            form = ChoreCreationForm()
        return render(request, 'flat/new_chore.html', {'form': form})
    else:
        return redirect('new-flat')


@login_required
def chores_list(request):
    if request.user.profile.active_flat is None:
        return redirect('new-flat')
    else:
        context = {
            'chores': request.user.profile.active_flat.chore_set.all()
        }
        return render(request, 'flat/chores_list.html', context)


def delete_chore(request, chore_id):
    chore = Chore.objects.get(pk=chore_id)
    chore.delete()
    return redirect(chores_list)


@login_required
def announcements(request):
    if request.user.profile.active_flat is None:
        return redirect('new-flat')
    else:
        context = {
            'announcements': request.user.profile.active_flat.announcement_set.all().order_by('-date'),
            'user': request.user
        }
        return render(request, 'flat/announcements.html', context)


def delete_announcement(request, ann_id):
    announcement = Announcement.objects.get(pk=ann_id)
    announcement.delete()
    return redirect(announcements)


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


@login_required
def your_chores(request):
    if request.user.profile.active_flat is None:
        return redirect('new-flat')
    else:
        flat_chores = request.user.profile.active_flat.chore_set.all()
        for chore in flat_chores:
            if timezone.now() - chore.last_made > timedelta(days=chore.period):
                print('hey')
                min_number = chore.chorecounter_set.aggregate(Min('number'))['number__min']
                #print(min_number)
                random_chore_counter = chore.chorecounter_set.all().filter(number=min_number)[0]
                random_chore_counter.number += 1
                random_chore_counter.save()
                #user = (ChoreCounter.objects.filter(chore=chore).values_list('user')
                #        .annotate(Min('number')).order_by('number')[0])
                SpecificChore(user=random_chore_counter.user, flat=request.user.profile.active_flat, start=timezone.now(),
                              end=timezone.now()+timedelta(days=chore.period), name=chore.name).save()
                chore.last_made = timezone.now()
                chore.save()
        your_active_chores = SpecificChore.objects.filter(flat=request.user.profile.active_flat, user=request.user,
                                                          completed=False).order_by('start')
        context = {
            'chores': your_active_chores
        }
        return render(request, 'flat/your_chores.html', context)


def completed_chore(request, chore_id):
    chore = SpecificChore.objects.get(pk=chore_id)
    chore.completed = True
    chore.save()
    return redirect(your_chores)


@login_required
def done_chores(request):
    if request.user.profile.active_flat is None:
        return redirect('new-flat')
    else:
        chores = SpecificChore.objects.filter(flat=request.user.profile.active_flat,
                                              completed=True).order_by('-start')
        context = {
            'chores': chores,
            'user': request.user
        }
        return render(request, 'flat/done_chores.html', context)
