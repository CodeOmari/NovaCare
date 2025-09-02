from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from user_management.app_forms import LoginForm
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def login_user(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('user_management:dashboard')
        messages.error(request, "Invalid username or password")
        return render(request, "login.html", {"form": form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account creation for {username} was successful!')
            return redirect('user_management:login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def signout_user(request):
    logout(request)
    return redirect('home')




@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('user_management:staff_dashboard')
    else:
        return redirect('user_management:patient_dashboard')


def patient_dashboard(request):
    context = {
        'username': request.user.username,
    }
    return render(request, 'patient_dashboard.html', context)

def staff_dashboard(request):
    context = {
        'username': request.user.username,
    }
    return render(request, 'staff_dashboard.html', context)
