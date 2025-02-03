from django.db import models

# Create your models here.

class Appointments(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=6)
    phone_number = models.IntegerField()
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=50)
    appointment_type = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = 'appointment'

