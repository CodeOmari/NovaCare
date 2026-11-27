from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

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
    quantity = models.PositiveIntegerField(default=1)
    dosage_frequency = models.CharField(max_length=200)
    duration_days = models.PositiveIntegerField(default=1)
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


def generate_invoice_number():
    return f'NC-INV-{uuid.uuid4().hex[:10].upper()}'

def generate_payment_reference():
    return f'NC-PAY-{uuid.uuid4().hex[:10].upper()}'

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='invoices')
    invoice_number = models.CharField(max_length=25, unique=True, default=generate_invoice_number, editable=False)
    service_name = models.CharField(max_length=200)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    date = models.DateField(default=timezone.localdate)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    invoice_pdf = models.FileField(upload_to='invoices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def amount_paid(self):
        return sum((payment.amount_paid for payment in self.payments.filter(status='SUCCESSFUL')),
            Decimal('0.00'))

    @property
    def amount_due(self):
        return max(self.total_amount - self.amount_paid, Decimal('0.00'))

    def __str__(self):
        return f'{self.invoice_number} - {self.patient}'

    class Meta:
        ordering = ['-date', '-created_at']
        

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('MPESA', 'M-Pesa'),
        ('CARD', 'Card'),
        ('CASH', 'Cash'),
        ('BANK', 'Bank Transfer'),
        ('OTHER', 'Other'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESSFUL', 'Successful'),
        ('FAILED', 'Failed'),
    ]
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='payments')
    payment_reference = models.CharField(max_length=25, unique=True, default=generate_payment_reference, editable=False)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='MPESA')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    date = models.DateTimeField(default=timezone.now)
    receipt_pdf = models.FileField(upload_to='payment_receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def service_name(self):
        return self.invoice.service_name

    @property
    def invoice_number(self):
        return self.invoice.invoice_number

    def __str__(self):
        return f'{self.payment_reference} - {self.amount_paid}'

    class Meta:
        ordering = ['-date', '-created_at']

class NursePatientAssignment(models.Model):
    nurse = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='nurse_patient_assignments', limit_choices_to={'role': 'NURSE'})
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='nurse_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nurse} - {self.patient}'


class Ward(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ward_number = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.ward_number}'


class Admission(models.Model):
    STATUS_CHOICES = [
        ('ADMITTED', 'Admitted'),
        ('DISCHARGED', 'Discharged'),
        ('TRANSFERRED', 'Transferred'),
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='admissions')
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, related_name='admissions')
    admitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='admissions_created')
    admission_date = models.DateTimeField(default=timezone.now)
    discharge_date = models.DateTimeField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ADMITTED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient} - {self.ward}'

    class Meta:
        ordering = ['-admission_date']


class VitalSign(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='vital_signs')
    nurse = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='recorded_vital_signs', limit_choices_to={'role': 'NURSE'})
    temperature = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(Decimal('25.0')), MaxValueValidator(Decimal('45.0'))])
    systolic_pressure = models.PositiveSmallIntegerField()
    diastolic_pressure = models.PositiveSmallIntegerField()
    pulse_rate = models.PositiveSmallIntegerField()
    respiratory_rate = models.PositiveSmallIntegerField()
    oxygen_saturation = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Vitals for {self.patient} - {self.recorded_at}'

    class Meta:
        ordering = ['-recorded_at']


class NursingTask(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('NORMAL', 'Normal'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]

    nurse = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='assigned_nursing_tasks', limit_choices_to={'role': 'NURSE'})
    patient = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT, related_name='patient_nursing_tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='NORMAL')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.patient}'

    class Meta:
        ordering = ['scheduled_date', 'scheduled_time']