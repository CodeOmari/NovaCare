from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('dashboard/', views.staff_dashboard, name='staff-dashboard'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor-appointments'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor-dashboard'),
    path('doctor/patients/', views.doctor_patients, name='doctor-patients'),
    path('doctor/patients/<int:patient_id>/', views.doctor_patient_detail, name='doctor-patient-detail'),
    path('doctor/consultations/', views.doctor_consultations, name='doctor-consultations'),

    path('receptionist/appointments/', views.receptionist_appointments, name='receptionist-appointments'),
    path('receptionist/dashboard/', views.receptionist_dashboard, name='receptionist-dashboard'),
    path('receptionist/doctors/', views.receptionist_doctors, name='receptionist-doctors'),
    path('receptionist/patients/', views.receptionist_patients, name='receptionist-patients'),
]