from django.urls import  path
from user_management import views

app_name = 'user_management'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]