from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone

# Create your models here.
class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    department = models.ForeignKey('main_app.Department', on_delete=models.PROTECT, related_name='appointments')
    doctor = models.ForeignKey('main_app.Doctor', on_delete=models.PROTECT, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    checked_in = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.patient} - {self.doctor} - {self.appointment_date}'

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']


class Consultation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    ]

    appointment = models.OneToOneField(Appointment, on_delete=models.PROTECT, related_name='consultation')
    symptoms = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    examination_notes = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Consultation - {self.appointment.patient} - {self.date.date()}'

    class Meta:
        ordering = ['-date']


def generate_prescription_number():
    return f"NC-RX-{uuid.uuid4().hex[:10].upper()}"

class Prescription(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    consultation = models.ForeignKey(Consultation, on_delete=models.PROTECT, related_name='prescriptions')
    medication_name = models.CharField(max_length=200)
    dosage_frequency = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    prescribed_date = models.DateField(default=timezone.localdate)
    prescription_number = models.CharField(max_length=20, unique=True, default=generate_prescription_number, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.medication_name} - {self.prescription_number}'

    class Meta:
        ordering = ['-prescribed_date', '-created_at']


def generate_lab_reference():
    return f'NC-LAB-{uuid.uuid4().hex[:10].upper()}'

class LaboratoryResult(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
    ]

    consultation = models.ForeignKey(Consultation, on_delete=models.PROTECT, related_name='laboratory_results')
    test_name = models.CharField(max_length=200)
    reference_number = models.CharField(max_length=25, unique=True, default=generate_lab_reference, editable=False)
    requested_date = models.DateField(default=timezone.localdate)
    result_summary = models.TextField(blank=True)
    report_file = models.FileField(upload_to='laboratory_reports/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    completed_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.test_name} - {self.reference_number}'

    class Meta:
        ordering = ['-requested_date', '-created_at']