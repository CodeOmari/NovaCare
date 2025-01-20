from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from main_app.app_forms import ChildForm, AdultForm, LoginForm, AdultAppointment
from main_app.models import AdultPatient, ChildPatient


# Create your views here.

def home(request):
    return render(request, 'Home.html')


def about(request):
    return render(request, 'About.html')


def careers(request):
    return render(request, 'Careers.html')


@login_required
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


@login_required
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


@login_required
def clients(request):
    return render(request, 'client_details.html')


def child_details(request):
    return None


def adult_details(request):
    return None


def update_adult_details(request):
    return None


def update_child_details(request):
    return None


def delete_child_details(request):
    return None


def delete_adult_details(request):
    return None


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
def book_adult_appointment(request, id):
    patient = get_object_or_404(AdultPatient, pk=id)

    if request.method == 'POST':
        form = AdultAppointment(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('home')
    else:
        form = AdultAppointment()
    return render(request, 'adult_appointment_form.html', {'form': form})


def book_child_appointment(request):
    return None