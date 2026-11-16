from django.shortcuts import render
from .departments import departments
from .general_medicine import services
from .cardiology import cardiologywork
from .dentistry import dentistrywork
from .dermatology import dermatologywork
from .gynecology import gynecologywork
from .orthopedics import orthopedicswork
from .pediatrics import pediatricwork
from .radiology import radiologywork
from .services import services
# Create your views here.
def home_page(request):
    return render(request, 'home-page.html', {'departments': departments, 'services': services})

def general_medicine(request):
    return render(request, 'general_medicine.html', {'services': services})

def pediatrics(request):
    return render(request, 'pediatrics.html', {'pediatricwork': pediatricwork})

def cardiology(request):
    return render(request, 'cardiology.html', {'cardiologywork': cardiologywork })

def dermatology(request):
    return render(request, 'dermatology.html', {'dermatologywork': dermatologywork })

def gynecology(request):
    return render(request, 'gynecology.html', { 'gynecologywork': gynecologywork})

def orthopedics(request):
    return render(request, 'orthopedics.html', {'orthopedicswork': orthopedicswork})

def dentistry(request):
    return render(request, 'dentistry.html', {'dentistrywork': dentistrywork})

def radiology(request):
    return render(request, 'radiology.html', {'radiologywork': radiologywork})