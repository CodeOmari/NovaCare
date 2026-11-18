from django.shortcuts import render
from .featured_departments import featured_departments
from .general_medicine import generalmedicine_work
from .cardiology import cardiologywork
from .dentistry import dentistrywork
from .dermatology import dermatologywork
from .gynecology import gynecologywork
from .orthopedics import orthopedicswork
from .pediatrics import pediatricwork
from .radiology import radiologywork
from .services import services
from .doctors import doctordetails
from .profile import profiledetails
from .choose_us import why_us
from .core_values import corevalues
from .facilities import facilities

from django.http import Http404
# Create your views here.
def home_page(request):
    return render(request, 'home-page.html', {'featured_departments': featured_departments, 'services': services, 'doctordetails': doctordetails, 'why_us': why_us })

def general_medicine(request):
    return render(request, 'general_medicine.html', {'generalmedicine_work': generalmedicine_work})

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


def about(request):
    return render(request, 'about.html', {'corevalues': corevalues, 'facilities': facilities })

def departments(request):
    return render(request, 'departments.html', {'featured_departments': featured_departments})

def doctors(request):
    return render(request, 'doctors.html', {'doctordetails': doctordetails, 'profiledetails': profiledetails })


def profile(request, slug):
    doctor = next(
        (doctor for doctor in profiledetails if doctor['slug'] == slug),
        None
    )

    if doctor is None:
        raise Http404("Doctor not found")

    return render(request, 'profile.html', {'doctor': doctor})

def contact(request):
    return render(request, 'contact.html')
