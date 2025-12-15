from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,  get_object_or_404
from user_management.app_forms import LoginForm, PasswordResetRequestForm, SetNewPasswordForm, CustomUserCreationForm, PersonalDetailsForm

from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from user_management.models import Details


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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account creation for {username} was successful!')
            return redirect('user_management:login')
    else:
        form = CustomUserCreationForm()
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
                reset_link = request.build_absolute_uri(
                    reverse('user_management:password_reset_confirm', args=[token])
                )

                html_content = f"""
                    <div>
                        <h2 style='color: #004f71; text-align: center;'> NovaCare </h2>

                        <p> Hi <strong>{user.username}</strong>, </p>

                        <p>
                            You requested a password reset. Click the link below to set a new password:
                        </p>

                        <p style='margin: 20px 0;'>
                            <a href="{reset_link}" style='display: inline-block; 
                                                   padding: 10px 15px; background-color: #004f71; color: white; 
                                                   text-decoration: none; border-radius: 5px;'>
                                Reset Password
                            </a>
                        </p>

                        <p>
                            If the above button doesn't work, copy and paste the following link into your browser:
                        </p>

                        <p>
                            <a href="{reset_link}">{reset_link}</a>
                        </p>

                        <p>
                            The link is valid for 30 minutes only.
                        </p>

                        <hr>

                        <p>
                            If you did not request a password reset, please ignore this email. <br>
                            &copy; {timezone.now().year} NovaCare. All rights reserved.
                        </p>
                    </div>
                """

                subject = "Password Reset Request"
                from_email = settings.DEFAULT_FROM_EMAIL
                to = [email]

                message = EmailMultiAlternatives(subject, "", from_email, to)
                message.attach_alternative(html_content, "text/html")
                message.send()


                messages.success(request, f'Your password reset link has been sent to {email}.')
                return redirect('user_management:login')
            except User.DoesNotExist:
                messages.error(request, f'No user found with the email {email}.')
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


@login_required
def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    details = (Details.objects.filter(user=user).order_by('-updated_at').first())
    if not details:
        details = Details.objects.create(user=user)
    return render(request, 'user_details.html', {'user': user, 'details': details})


@login_required
def add_details(request):
    try:
        details = Details.objects.get(user=request.user)
    except Details.DoesNotExist:
        details= None

    if request.method == "POST":
        form = PersonalDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            personal_details = form.save(commit=False)
            personal_details.user = request.user
            personal_details.save()
            messages.success(request, "Details updated successfully")
            return redirect('user_management:dashboard')
    else:
        form = PersonalDetailsForm(instance=details)
    return render(request, 'user_update_form.html', {"form": form})
