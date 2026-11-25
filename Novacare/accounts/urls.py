from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='patient-dashboard'),
    path('appointments/', views.patient_appointments, name='patient-appointments'),
    path('medical-records/', views.medical_records, name='medical-records'),
    path('prescriptions/', views.patient_prescriptions, name='patient-prescriptions'),
    path('laboratory-results/', views.patient_laboratory_results, name='patient-laboratory-results'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)