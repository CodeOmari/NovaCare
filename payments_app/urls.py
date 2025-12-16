from django.urls import path
from payments_app import views

app_name = 'payments_app'


urlpatterns = [
    path('payment/', views.payment_page, name='payment_page'),
    path('payment/<int:id>/', views.payment, name='payment'),
    path('callback/', views.callback, name='trigger'),
]