from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrWorkIDBackend(ModelBackend):
    STAFF_ROLES = [
        'DOCTOR',
        'NURSE',
        'NURSE MANAGER',
        'PHARMACIST',
        'RECEPTIONIST',
        'LABORATORY TECHNICIAN',
        'ACCOUNTANT',
        'ADMISSIONS OFFICER',
        'ADMINISTRATOR',
        'STAFF',
    ]

    EMAIL_ROLES = ['PATIENT', 'ADMIN',]

    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        identifier = (username or kwargs.get('email') or kwargs.get('work_id'))

        if not identifier or not password:
            return None

        user = None

        try:
            user = User.objects.get(email__iexact=identifier)

            if user.role not in self.EMAIL_ROLES:
                user = None

        except (User.DoesNotExist, User.MultipleObjectsReturned):
            pass

        if user is None:
            try:
                user = User.objects.get(work_id__iexact=identifier)

                if user.role not in self.STAFF_ROLES:
                    user = None

            except (User.DoesNotExist, User.MultipleObjectsReturned):
                pass

        if (user is not None and user.check_password(password) and self.user_can_authenticate(user)):
            return user

        return None