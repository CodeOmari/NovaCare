"""
URL configuration for NovaCare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from main_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('emergency/services/', views.emergency_services, name='emergency_services'),
    path('inpatient/services/', views.inpatient_services, name='inpatient_services'),
    path('outpatient/services/', views.outpatient_services, name='outpatient_services'),
    path('surgical/services/', views.surgical_services, name='surgical_services'),
    path('maternity/services/', views.maternity_services, name='maternity_services'),
    path('careers/', views.careers, name='careers'),


    path('users/', include('user_management.urls')),

    path('admin/', admin.site.urls),
]
