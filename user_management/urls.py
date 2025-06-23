from django.urls import  path
from user_management import views

app_name = 'user_management'

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),


    path('portal/', views.dashboard, name='dashboard'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('users/', views.patient_dashboard, name='patient_dashboard'),
]