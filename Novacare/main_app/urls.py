from django.urls import path
from main_app import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
]