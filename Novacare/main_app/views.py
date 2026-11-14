from django.shortcuts import render
from .departments import departments
# Create your views here.
def home_page(request):
    return render(request, 'home-page.html', {'departments': departments})

def general_medicine(request):
    return render(request, 'general_medicine.html')

def pediatrics(request):
    return render(request, 'pediatrics.html')

def cardiology(request):
    return render(request, 'cardiology.html')

def dermatology(request):
    return render(request, 'dermatology.html')

def gynecology(request):
    return render(request, 'gynecology.html')

def orthopedics(request):
    return render(request, 'orthopedics.html')

def dentistry(request):
    return render(request, 'dentistry.html')

def radiology(request):
    return render(request, 'radiology.html')