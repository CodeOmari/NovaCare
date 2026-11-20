from django.shortcuts import render, get_object_or_404
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
from .models import Department
from django.http import Http404
from .models import Department, Doctor
# Create your views here.
def home_page(request):
    return render(request, 'home-page.html', {'featured_departments': featured_departments, 'services': services, 'doctordetails': doctordetails, 'why_us': why_us })

def general_medicine(request):
    department = get_object_or_404(Department, slug='general-medicine')
    doctors = Doctor.objects.filter(department=department, is_available=True)
    services = department.services.all()
    return render(request, 'general_medicine.html', {'department': department, 'doctors': doctors, 'services': services,})

def pediatrics(request):
    department = get_object_or_404(Department,slug='pediatrics')
    doctors = Doctor.objects.filter(department=department,is_available=True)
    services = department.services.all()
    return render(request, 'pediatrics.html', {'department': department,'doctors': doctors,'services': services,'pediatricwork': pediatricwork,})

def cardiology(request):
    department = get_object_or_404(Department,slug='cardiology')
    doctors = Doctor.objects.filter(department=department,is_available=True)
    services = department.services.all()
    return render(request, 'cardiology.html', {'department': department,'doctors': doctors,'services': services,'cardiologywork': cardiologywork,})

def dermatology(request):
    department = get_object_or_404(Department,slug='dermatology')
    doctors = Doctor.objects.filter(department=department,is_available=True)
    services = department.services.all()
    return render(request, 'dermatology.html', {'department': department,'doctors': doctors,'services': services,'dermatologywork': dermatologywork,})

def gynecology(request):
    department = get_object_or_404(Department,slug='gynecology')
    doctors = Doctor.objects.filter(department=department,is_available=True)
    services = department.services.all()
    return render(request, 'gynecology.html', {'department': department,'doctors': doctors,'services': services,'gynecologywork': gynecologywork,})

def orthopedics(request):
    department = get_object_or_404(Department,slug='orthopedics')
    doctors = Doctor.objects.filter(department=department, is_available=True)
    services = department.services.all()
    return render(request, 'orthopedics.html', {'department': department,'doctors': doctors,'services': services,'orthopedicswork': orthopedicswork,})


def dentistry(request):
    department = get_object_or_404(Department,slug='dentistry')
    doctors = Doctor.objects.filter(department=department,is_available=True)
    services = department.services.all()
    return render(request, 'dentistry.html', {'department': department,'doctors': doctors,'services': services,'dentistrywork': dentistrywork,})

def radiology(request):
    department = get_object_or_404(Department,slug='radiology')
    doctors = Doctor.objects.filter(department=department,is_available=True)
    services = department.services.all()
    return render(request, 'radiology.html', {'department': department,'doctors': doctors,'services': services,'radiologywork': radiologywork,})

def about(request):
    return render(request, 'about.html', {'corevalues': corevalues, 'facilities': facilities })

def departments(request):
    departments = Department.objects.all()

    department_urls = {
        'general-medicine': 'general_medicine',
        'pediatrics': 'pediatrics',
        'cardiology': 'cardiology',
        'dermatology': 'dermatology',
        'gynecology': 'gynecology',
        'orthopedics': 'orthopedics',
        'dentistry': 'dentistry',
        'radiology': 'radiology',
    }

    for department in departments:
        department.url_name = department_urls.get(department.slug)
    return render(request, 'departments.html', {'featured_departments': departments})

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