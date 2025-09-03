from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from user_management.app_forms import LoginForm, PasswordResetRequestForm, SetNewPasswordForm
from django.contrib.auth.forms import UserCreationForm

from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password


signer = TimestampSigner() # creates signed tokens


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

# Request reset via email
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = signer.sign(user.pk) # sign user id
                reset_link = request.build_absolute_uri(f"/reset-password-confirm/{token}")

                # send email
                send_mail("Password Reset Request",
                          f"Click the link below to reset your password:\n{reset_link}",
                          settings.DEFAULT_FROM_EMAIL,
                          [email],
                          fail_silently=False,
                )
                messages.success(request, f'Your password reset link has been sent to {email}.')
                return redirect('user_management:login')
            except User.DoesNotExist:
                messages.error(request, f'No user found with email {email}.')
    else:
        form = PasswordResetRequestForm()
    return render(request, "password_reset_request.html", {'form': form})


# Reset password using token
def password_reset_confirm(request, token):
    try:
        user_id = signer.unsign(token, max_age=3600) # token id valid for 1 hour
        user = User.objects.get(pk=user_id)
    except (BadSignature, SignatureExpired, User.DoesNotExist):
        messages.error(request, 'Invalid or expired reset link.')
        return redirect("user_management:password_reset_request")

    if request.method == "POST":
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user_password = form.cleaned_data["new_password"]
            user.password = make_password(user_password)
            user.save()
            messages.success(request, 'Password updated successfully!')
            return redirect('user_management:login')
    else:
        form = SetNewPasswordForm()
    return render(request, 'password_reset_confirm.html', {'form': form})



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
