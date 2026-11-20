from django.urls import path
from main_app import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('departments/general-medicine', views.general_medicine, name='general_medicine'),
    path('departments/pediatrics', views.pediatrics, name='pediatrics'),
    path('departments/cardiology', views.cardiology, name='cardiology'),
    path('departments/dermatology', views.dermatology, name='dermatology'),
    path('departments/gynecology', views.gynecology, name='gynecology'),
    path('departments/orthopedics', views.orthopedics, name='orthopedics'),
    path('departments/dentistry', views.dentistry, name='dentistry'),
    path('departments/radiology', views.radiology, name='radiology'),

    path('about', views.about, name='about_us'),
    path('departments', views.departments, name='departments'),
    path('doctors', views.doctors, name='doctors'),
    path('doctors/<slug:slug>', views.profile, name='doctor_profile'),
    path('contact', views.contact, name='contact-us'),
]