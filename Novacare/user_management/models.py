import secrets
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

class UserManager(BaseUserManager):
    STAFF_ROLES = [
        'DOCTOR',
        'NURSE',
        'PHARMACIST',
        'RECEPTIONIST',
        'ACCOUNTANT',
        'LABORATORY TECHNICIAN',
        'ADMINISTRATOR',
        'STAFF',
    ]

    def create_user(self, email=None, password=None, **extra_fields):
        role = extra_fields.get('role', 'PATIENT')
        if (not email and not extra_fields.get('work_id') and role not in self.STAFF_ROLES and role != 'ADMIN'):
            raise ValueError("An email or work ID is required.")

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'ADMINISTRATOR')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)

    def create_staff_user(self, password, role='RECEPTIONIST', **extra_fields):
        if role not in [
            'DOCTOR',
            'NURSE',
            'PHARMACIST',
            'RECEPTIONIST',
            'LABORATORY TECHNICIAN',
            'ACCOUNTANT',
            'ADMINISTRATOR',
        ]:
            raise ValueError("Invalid staff role.")

        extra_fields['role'] = role
        extra_fields['is_staff'] = False

        return self.create_user(password=password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('PHARMACIST', 'Pharmacist'),
        ('RECEPTIONIST', 'Receptionist'),
        ('ACCOUNTANT', 'Accountant'),
        ('LABORATORY TECHNICIAN', 'Laboratory Technician'),
        ('ADMINISTRATOR', 'Administrator'),

        ('STAFF', 'Legacy Staff'),
        ('ADMIN', 'Legacy Administrator'),
    ]

    email = models.EmailField(unique=True, null=True, blank=True)
    work_id = models.CharField(max_length=30, unique=True, null=True, blank=True)
    role = models.CharField(max_length=25, choices=ROLE_CHOICES, default='PATIENT')
    doctor_profile = models.OneToOneField('main_app.Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_account')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        staff_roles = [
            'DOCTOR',
            'NURSE',
            'PHARMACIST',
            'RECEPTIONIST',
            'ACCOUNTANT',
            'LABORATORY TECHNICIAN',
            'ADMINISTRATOR',
            'STAFF',
        ]

        if self.role in staff_roles and not self.work_id:
            while True:
                candidate = f"NC-STAFF-{secrets.token_hex(4).upper()}"

                if not User.objects.filter(work_id=candidate).exists():
                    self.work_id = candidate
                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email or self.work_id or str(self.pk)