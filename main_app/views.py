from django.shortcuts import render



# Create your views here.

def home(request):
    return render(request, 'Home.html')


def about(request):
    return render(request, 'About.html')


def careers(request):
    return render(request, 'Careers.html')

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
