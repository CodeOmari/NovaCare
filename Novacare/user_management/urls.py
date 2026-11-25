from django.urls import path
from user_management import views
from django.contrib.auth.views import LogoutView

app_name = 'user_management'

urlpatterns = [
    path('patient/login', views.patient_login, name="patient-login"),
    path('patient/reset-password', views.patient_reset_password, name='forgot-password'),
    path('patient/register', views.create_account, name="create-account"), 

    path('staff/login', views.staff_login, name='staff-login'),
    path("staff/reset-password", views.staff_reset_password, name="reset-password"),

    path('logout/', LogoutView.as_view(), name='logout'),
]