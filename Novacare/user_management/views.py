from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import PatientRegistrationForm


STAFF_ROLES = [
    'DOCTOR',
    'NURSE',
    'PHARMACIST',
    'RECEPTIONIST',
    'ACCOUNTANT',
    'LABORATORY TECHNICIAN',
    'ADMINISTRATOR',
    'STAFF',
]
def create_account(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('user_management:patient-login')
    else:
        form = PatientRegistrationForm()
    return render(request, 'create-account.html', {'form': form})

def staff_login(request):
    error = None

    if request.method == 'POST':
        work_id = request.POST.get('work_id', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=work_id, password=password)

        if user is not None and user.role in STAFF_ROLES:
            login(request, user)

            if user.role == 'RECEPTIONIST':
                return redirect('staff:receptionist-dashboard')

            elif user.role == 'DOCTOR':
                return redirect('staff:doctor-dashboard')

            return redirect('staff:staff-dashboard')

        error = 'Invalid Work ID or password. Please try again.'
    return render(request, 'staff-login.html', {'error': error})


def patient_login(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=email, password=password)

        if user is not None and user.role == 'PATIENT':
            login(request, user)
            return redirect('accounts:patient-dashboard')

        error = 'Invalid email or password. Please try again.'

    return render(request, 'patient-login.html', {'error': error})


def staff_reset_password(request):
    return render(request, 'forgot-password.html')


def patient_reset_password(request):
    return render(request, 'patient-reset-password.html')
