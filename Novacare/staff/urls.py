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
    path('doctor/consultations/new/', views.new_consultation, name='new-consultation'),
    path('doctor/consultations/<int:consultation_id>/', views.doctor_consultation_detail, name='doctor-consultation-detail'),
    path('doctor/consultations/<int:consultation_id>/edit/', views.edit_consultation, name='edit-consultation'),
    path('doctor/consultations/<int:consultation_id>/prescription/', views.issue_prescription, name='issue-prescription'),

    path('receptionist/appointments/', views.receptionist_appointments, name='receptionist-appointments'),
    path('receptionist/dashboard/', views.receptionist_dashboard, name='receptionist-dashboard'),
    path('receptionist/doctors/', views.receptionist_doctors, name='receptionist-doctors'),
    path('receptionist/patients/', views.receptionist_patients, name='receptionist-patients'),

    path('accountant/dashboard/', views.accountant_dashboard, name='accountant-dashboard'),

    path('nurse/dashboard/', views.nurse_dashboard, name='nurse-dashboard'),
    path('nurse/patients/', views.nurse_patients, name='nurse-patients'),
    path('nurse-manager/dashboard/', views.nurse_manager_dashboard, name='nurse-manager-dashboard'),
    path('nurse-manager/assignments/', views.nurse_manager_assignments, name='nurse-manager-assignments'),
    path('nurse-manager/search/', views.nurse_manager_search, name='nurse-manager-search'),
]