from django.db import models

# Create your models here.

class AdultPatient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = 'adult_patients'


class ChildPatient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    parent_first_name = models.CharField(max_length=30)
    parent_last_name = models.CharField(max_length=30)
    parent_gender = models.CharField(max_length=10)
    parent_phone_number = models.CharField(max_length=10)
    relationship = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = 'child_patients'


class AdultAppointments(models.Model):
    patient = models.ForeignKey(AdultPatient, on_delete=models.CASCADE)
    age = models.IntegerField()
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=50)
    appointment_type = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.patient.first_name} {self.patient.last_name}'

    class Meta:
        db_table = 'adult_appointments'


class ChildAppointments(models.Model):
    patient = models.ForeignKey(ChildPatient, on_delete=models.CASCADE)
    age = models.IntegerField()
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=50)
    appointment_type = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.patient.first_name} {self.patient.last_name}'

    class Meta:
        db_table = 'child_appointments'
