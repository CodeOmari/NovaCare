from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from main_app.app_forms import ChildForm, AdultForm
from main_app.models import AdultPatient, ChildPatient


# Create your views here.
def home(request):
    return render(request, 'Home.html')

def about(request):
    return render(request, 'About.html')

def careers(request):
    return render(request, 'Careers.html')

def add_client(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration completed successfully!')
            return redirect('home')
    else:
        form = ChildForm()
    return render(request, 'children_form.html', {'form': form})


def add_adult_client(request):
    if request.method == 'POST':
        form = AdultForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration completed successfully!')
            return redirect('home')
    else:
        form = AdultForm()
    return render(request, 'adult_form.html', {'form': form})