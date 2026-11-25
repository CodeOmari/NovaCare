from django.contrib import admin
from .models import PatientProfile, Appointment


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