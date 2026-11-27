from django.contrib import admin
from .models import (
    NursePatientAssignment, Ward, Admission, VitalSign, NursingTask, PatientProfile, Appointment, Invoice, Payment)

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'get_email', 'phone', 'created_at',)
    search_fields = ('full_name', 'phone', 'user__email',)
    readonly_fields = ('created_at', 'updated_at',)
    ordering = ('full_name',)
    list_per_page = 25

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email Address'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(user__role='PATIENT')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            from django.contrib.auth import get_user_model

            User = get_user_model()
            kwargs['queryset'] = User.objects.filter(role='PATIENT')

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'department', 'doctor', 'appointment_date', 'appointment_time', 'status',)
    list_filter = ('status', 'department', 'appointment_date',)
    search_fields = ('patient__email', 'doctor__name', 'department__name',)
    ordering = ('-appointment_date', '-appointment_time')
    list_per_page = 25


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'patient', 'service_name', 'total_amount', 'status', 'date',)
    list_filter = ('status', 'date')
    search_fields = ('invoice_number', 'patient__email', 'service_name',)
    readonly_fields = ('invoice_number', 'created_at', 'updated_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_reference', 'invoice', 'amount_paid', 'payment_method', 'status', 'date',)
    list_filter = ('status', 'payment_method', 'date')
    search_fields = ('payment_reference', 'invoice__invoice_number',)
    readonly_fields = ('payment_reference', 'created_at')


@admin.register(NursePatientAssignment)
class NursePatientAssignmentAdmin(admin.ModelAdmin):
    list_display = ('nurse', 'patient', 'assigned_at', 'is_active')
    list_filter = ('is_active', 'assigned_at')
    search_fields = ('nurse__email', 'patient__email')
    list_editable = ('is_active',)


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward_number', 'capacity', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'ward_number')


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'ward', 'admission_date', 'discharge_date', 'status')
    list_filter = ('status', 'ward', 'admission_date')
    search_fields = ('patient__email', 'ward__name')
    date_hierarchy = 'admission_date'


@admin.register(VitalSign)
class VitalSignAdmin(admin.ModelAdmin):
    list_display = ('patient', 'nurse', 'temperature', 'systolic_pressure', 'diastolic_pressure', 'pulse_rate', 'oxygen_saturation', 'recorded_at',)
    list_filter = ('recorded_at', 'nurse')
    search_fields = ('patient__email', 'nurse__email')
    date_hierarchy = 'recorded_at'


@admin.register(NursingTask)
class NursingTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'nurse', 'patient', 'scheduled_date', 'scheduled_time', 'priority', 'status',)
    list_filter = ('status', 'priority', 'scheduled_date')
    search_fields = ('title', 'nurse__email', 'patient__email')
    date_hierarchy = 'scheduled_date'