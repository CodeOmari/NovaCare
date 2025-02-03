from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from main_app.app_forms import  LoginForm, Appointment


# Create your views here.

def home(request):
    return render(request, 'Home.html')


def about(request):
    return render(request, 'About.html')


def careers(request):
    return render(request, 'Careers.html')


def login_user(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login_form.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
        messages.error(request, "Invalid username or password")
        return render(request, "login_form.html", {"form": form})


@login_required
def signout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account creation for {username} was successful!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'Register.html', {'form': form})

def emergency_services(request):
    return render(request, 'emergency.html')


def inpatient_services(request):
    return render(request, 'inpatient.html')


def outpatient_services(request):
    return render(request, 'outpatient.html')


def surgical_services(request):
    return render(request, 'surgical.html')


def maternity_services(request):
    return render(request, 'maternity.html')

@login_required
def book_appointment(request):
    return None


