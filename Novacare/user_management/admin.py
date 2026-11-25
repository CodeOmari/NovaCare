from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db import models
from main_app.models import Doctor

User = get_user_model()

STAFF_ROLE_CHOICES = [
    ('DOCTOR', 'Doctor'),
    ('NURSE', 'Nurse'),
    ('PHARMACIST', 'Pharmacist'),
    ('RECEPTIONIST', 'Receptionist'),
    ('ACCOUNTANT', 'Accountant'),
    ('LABORATORY TECHNICIAN', 'Laboratory Technician'),
    ('ADMINISTRATOR', 'Administrator'),
]

class StaffCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=STAFF_ROLE_CHOICES)
    doctor_profile = forms.ModelChoiceField(queryset=Doctor.objects.all(), required=False, empty_label="Select a doctor profile")

    class Meta:
        model = User
        fields = ('email', 'role', 'doctor_profile')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['doctor_profile'].queryset = Doctor.objects.filter(user_account__isnull=True)

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        role = cleaned_data.get('role')
        doctor_profile = cleaned_data.get('doctor_profile')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        if role == 'DOCTOR' and not doctor_profile:
            self.add_error('doctor_profile', "A doctor account must be linked to a doctor profile.")

        if role != 'DOCTOR' and doctor_profile:
            self.add_error('doctor_profile', "Only doctor accounts can have a doctor profile.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.role = self.cleaned_data['role']
        user.is_staff = False
        user.is_superuser = False

        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


class StaffChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Password")

    class Meta:
        model = User
        fields = (
            'email',
            'work_id',
            'role',
            'doctor_profile',
            'is_active',
            'groups',
            'user_permissions',
            'password',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['doctor_profile'].queryset = Doctor.objects.filter(models.Q(user_account__isnull=True) | models.Q(user_account=self.instance))

    def clean(self):
        cleaned_data = super().clean()

        role = cleaned_data.get('role')
        doctor_profile = cleaned_data.get('doctor_profile')

        if role == 'DOCTOR' and not doctor_profile:
            self.add_error('doctor_profile', "A doctor account must be linked to a doctor profile.")

        if role != 'DOCTOR' and doctor_profile:
            self.add_error('doctor_profile', "Only doctor accounts can have a doctor profile.")

        return cleaned_data


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'work_id',
        'email',
        'role',
        'doctor_profile',
        'is_active',
    )

    list_filter = (
        'role',
        'is_active',
    )

    search_fields = (
        'work_id',
        'email',
    )

    readonly_fields = ('work_id',)

    filter_horizontal = (
        'groups',
        'user_permissions',
    )

    ordering = ('work_id',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        return queryset.filter(
            role__in=[
                'DOCTOR',
                'NURSE',
                'PHARMACIST',
                'RECEPTIONIST',
                'ACCOUNTANT',
                'LABORATORY TECHNICIAN',
                'ADMINISTRATOR',
                'STAFF',
                'ADMIN',
            ]
        )

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = StaffCreationForm
        else:
            kwargs['form'] = StaffChangeForm

        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return (
                ('Staff Account Details', {
                    'fields': (
                        'email',
                        'role',
                        'doctor_profile',
                        'password1',
                        'password2',
                    )
                }),
            )

        return (
            ('Staff Information', {
                'fields': (
                    'email',
                    'work_id',
                    'role',
                    'doctor_profile',
                    'is_active',
                )
            }),
            ('Access Permissions', {
                'fields': (
                    'groups',
                    'user_permissions',
                )
            }),
            ('Security', {
                'fields': ('password',)
            }),
        )

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
