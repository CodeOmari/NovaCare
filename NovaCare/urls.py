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
from django.urls import path

from main_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('careers/', views.careers, name='careers'),
    path('clients/', views.clients, name='clients'),
    path('child/personal/details/<int:child_patients_id>', views.child_details, name='child_details'),
    path('adult/personal/details/<int:adult_patients_id>', views.adult_details, name='adult_details'),
    path('update/details/<int:adult_patients_id>', views.update_adult_details, name='update_adult_details'),
    path('update/details/<int:child_patients_id>', views.update_child_details, name='update_child_details'),
    path('delete/child/<int:child_patients_id>', views.delete_child_details, name='delete_child_details'),
    path('delete/adult/<int:adult_patients_id>', views.delete_adult_details, name='delete_adult_details'),
    path('add/child/client', views.add_client, name='add_client'),
    path('add/client', views.add_adult_client, name='add_adult_client'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.signout, name='logout'),
    path('register/', views.register, name='register'),
    path('admin/', admin.site.urls),
]
