from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('departments/general-medicine', views.general_medicine, name='general-medicine'),
    path('departments/pediatrics', views.pediatrics, name='pediatrics'),
    path('departments/cardiology', views.cardiology, name='cardiology'),
    path('departments/dermatology', views.dermatology, name='dermatology'),
    path('departments/gynecology', views.gynecology, name='gynecology'),
    path('departments/orthopedics', views.orthopedics, name='orthopedics'),
    path('departments/dentistry', views.dentistry, name='dentistry'),
    path('departments/radiology', views.radiology, name='radiology'),
]