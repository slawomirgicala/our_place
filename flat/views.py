from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import FlatCreationForm
from django.contrib import messages

# Create your views here.


@login_required
def home(request):
#   if request.user.is_authenticated():
        if request.user.profile.active_flat is None:
            return redirect('new-flat')
        else:
            context = {
                'profiles': request.user.profile.active_flat.profiles.all()
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
            return redirect('flat-home') #strona glowna mieszkania

    else:
        form = FlatCreationForm()
    return render(request, 'flat/new_flat.html', {'form': form})
