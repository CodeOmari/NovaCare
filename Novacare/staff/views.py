from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from main_app.models import Doctor
from accounts.models import Appointment, PatientProfile, Consultation
from django.db.models import Prefetch, OuterRef, Subquery
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.db.models import Q

STAFF_ROLES = [
    'DOCTOR',
    'NURSE',
    'PHARMACIST',
    'RECEPTIONIST',
    'LABORATORY TECHNICIAN',
    'ACCOUNTANT',
    'ADMINISTRATOR',
    'STAFF',
]

@login_required(login_url='user_management:staff-login')
def staff_dashboard(request):
    if request.user.role not in STAFF_ROLES:
        raise PermissionDenied
    return render(request, 'staff-dashboard.html')


@login_required(login_url='user_management:staff-login')
def doctor_appointments(request):
    if request.user.role != 'DOCTOR':
        raise PermissionDenied

    doctor = request.user.doctor_profile

    appointments = Appointment.objects.select_related('patient', 'patient__patient_profile', 'department', 'doctor').filter(doctor=doctor)

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        action = request.POST.get('action')

        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

        if action == 'update_status':
            new_status = request.POST.get('status')

            if appointment.status in ['PENDING', 'APPROVED']:
                if new_status in ['APPROVED', 'REJECTED']:
                    appointment.status = new_status
                    appointment.save(update_fields=['status', 'updated_at'])

                    messages.success(request, f'Appointment successfully marked as {appointment.get_status_display().lower()}.')
                else:
                    messages.error(request, 'Invalid appointment status.')

            else:
                messages.error(request, 'Only pending or approved appointments can be updated.')

        elif action == 'check_in':
            if appointment.status == 'APPROVED' and not appointment.checked_in:
                appointment.checked_in = True
                appointment.save(update_fields=['checked_in', 'updated_at'])

                messages.success(request, 'Patient successfully checked in.')

            else:
                messages.error(request, 'This patient cannot be checked in.')

        elif action == 'cancel':
            if appointment.status in ['PENDING', 'APPROVED']:
                appointment.status = 'CANCELLED'
                appointment.save(update_fields=['status', 'updated_at'])

                messages.success(request, 'Appointment successfully cancelled.')

            else:
                messages.error(request, 'This appointment cannot be cancelled.')

        return redirect('staff:doctor-appointments')

    selected_status = request.GET.get('status', '').upper()

    valid_statuses = [
        choice[0] for choice in Appointment.STATUS_CHOICES
    ]

    if selected_status in valid_statuses:
        appointments = appointments.filter(status=selected_status)
    else:
        selected_status = ''

    context = {
        'appointments': appointments,
        'selected_status': selected_status,
        'status_choices': Appointment.STATUS_CHOICES,
        'doctor': doctor,
        'today': timezone.localdate(),
    }

    return render(request, 'doctor-appointments.html', context)


@login_required(login_url='user_management:staff-login')
def doctor_patients(request):
    if request.user.role != 'DOCTOR':
        raise PermissionDenied

    doctor = request.user.doctor_profile

    if not doctor:
        raise PermissionDenied

    latest_appointment = Appointment.objects.filter(patient=OuterRef('user_id'), doctor=doctor).order_by(
        '-appointment_date',
        '-appointment_time',
        '-created_at')

    patients = PatientProfile.objects.filter(user__appointments__doctor=doctor).annotate(
        latest_appointment_status=Subquery(
            latest_appointment.values('status')[:1])
    ).select_related(
        'user'
    ).prefetch_related(
        Prefetch(
            'user__appointments',
            queryset=Appointment.objects.filter(
                doctor=doctor
            ).select_related(
                'doctor'
            ).order_by(
                '-appointment_date',
                '-appointment_time',
                '-created_at'
            ),
            to_attr='doctor_appointments'
        )
    ).distinct().order_by('full_name')

    search_query = request.GET.get('search', '').strip()

    if search_query:
        patients = patients.filter(
            Q(full_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )

    selected_status = request.GET.get('status', '').upper()

    valid_statuses = [
        choice[0] for choice in Appointment.STATUS_CHOICES
    ]

    if selected_status in valid_statuses:
        patients = patients.filter(latest_appointment_status=selected_status)
    else:
        selected_status = ''

    context = {
        'doctor': doctor,
        'patients': patients,
        'search_query': search_query,
        'selected_status': selected_status,
        'status_choices': Appointment.STATUS_CHOICES,
        'today': timezone.localdate(),
    }
    return render(request, 'doctor-patients.html', context)


@login_required(login_url='user_management:staff-login')
def doctor_patient_detail(request, patient_id):
    if request.user.role != 'DOCTOR':
        raise PermissionDenied

    doctor = request.user.doctor_profile

    if not doctor:
        raise PermissionDenied

    patient = get_object_or_404(PatientProfile.objects.filter(user__appointments__doctor=doctor).distinct(),
        pk=patient_id
    )

    appointments = Appointment.objects.filter(
        patient=patient.user,
        doctor=doctor
    ).select_related(
        'department'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    context = {
        'doctor': doctor,
        'patient': patient,
        'appointments': appointments,
    }

    return render(request, 'doctor-patient-details.html', context)

@login_required(login_url='user_management:staff-login')
def receptionist_appointments(request):
    if request.user.role != 'RECEPTIONIST':
        raise PermissionDenied

    appointments = Appointment.objects.select_related('patient', 'patient__patient_profile', 'department', 'doctor').filter(status='APPROVED')

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')

        appointment = get_object_or_404(Appointment, id=appointment_id, status='APPROVED')

        if not appointment.checked_in:
            appointment.checked_in = True
            appointment.save(update_fields=['checked_in', 'updated_at'])
            messages.success(request, 'Patient successfully checked in.')
        else:
            messages.info(request, 'This patient has already checked in.')

        return redirect('staff:receptionist-appointments')

    selected_date = request.GET.get('date', '')
    selected_doctor = request.GET.get('doctor', '')
    search_query = request.GET.get('search', '').strip()

    if selected_date:
        parsed_date = parse_date(selected_date)

        if parsed_date:
            appointments = appointments.filter(appointment_date=parsed_date)
        else:
            selected_date = ''

    if selected_doctor.isdigit():
        appointments = appointments.filter(doctor_id=selected_doctor)
    else:
        selected_doctor = ''

    if search_query:
        appointments = appointments.filter(
            Q(patient__patient_profile__full_name__icontains=search_query) |
            Q(doctor__name__icontains=search_query) |
            Q(department__name__icontains=search_query)
        )

    doctors = Doctor.objects.all().order_by('name')
    return render(request, 'receptionist-appointments.html', {'appointments': appointments, 'selected_date': selected_date, 'selected_doctor': selected_doctor, 'search_query': search_query, 'doctors': doctors, 'today': timezone.localdate(),})

@login_required(login_url='user_management:staff-login')
def receptionist_dashboard(request):
    if request.user.role != 'RECEPTIONIST':
        raise PermissionDenied

    today = timezone.localdate()

    todays_appointments = (Appointment.objects.select_related('patient', 'patient__patient_profile', 'doctor','department')
        .filter(appointment_date=today).order_by('appointment_time'))

    recent_patients = (PatientProfile.objects.select_related('user').prefetch_related(
            Prefetch(
                'user__appointments',
                queryset=Appointment.objects.select_related(
                    'doctor'
                ).order_by('-appointment_date', '-appointment_time'),
                to_attr='recent_appointments'
            )
        )
        .order_by('-created_at')[:4]
    )

    context = {
        'today': today,
        'total_patients': PatientProfile.objects.count(),
        'todays_appointments_count': todays_appointments.count(),
        'pending_appointments_count': Appointment.objects.filter(
            status='PENDING'
        ).count(),
        'recently_registered_count': PatientProfile.objects.filter(
            created_at__date=today
        ).count(),
        'todays_appointments': todays_appointments,
        'recent_patients': recent_patients,
    }
    return render(request, 'receptionist-dashboard.html', context)


@login_required(login_url='user_management:staff-login')
def doctor_dashboard(request):
    if request.user.role != 'DOCTOR':
        raise PermissionDenied

    doctor = request.user.doctor_profile
    today = timezone.localdate()

    doctor_appointments = Appointment.objects.filter(doctor=doctor)

    todays_appointments = (doctor_appointments.select_related('patient', 'patient__patient_profile', 'doctor','department')
        .filter(appointment_date=today).order_by('appointment_time'))

    recent_activity = (doctor_appointments.filter(status='COMPLETED').select_related('patient').order_by('-updated_at')[:5])

    context = {
        'doctor': doctor,
        'today': today,

        'assigned_patients_count': doctor_appointments.values(
            'patient'
        ).distinct().count(),

        'todays_appointments_count': todays_appointments.count(),

        'pending_consultations_count': doctor_appointments.filter(
            status='PENDING'
        ).count(),

        'completed_consultations_count': doctor_appointments.filter(
            status='COMPLETED'
        ).count(),

        'todays_appointments': todays_appointments,
        'recent_activity': recent_activity,
    }

    return render(request,'doctor-dashboard.html', context)

@login_required(login_url='user_management:staff-login')
def doctor_consultations(request):
    if request.user.role != 'DOCTOR':
        raise PermissionDenied

    doctor = request.user.doctor_profile

    consultations = Consultation.objects.select_related(
        'appointment',
        'appointment__patient',
        'appointment__patient__patient_profile',
        'appointment__doctor',
        'appointment__department'
    ).filter(
        appointment__doctor=doctor
    )

    context = {
        'doctor': doctor,
        'consultations': consultations,
        'today': timezone.localdate(),
    }

    return render(request, 'doctor-consultations.html', context)


@login_required(login_url='user_management:staff-login')
def receptionist_doctors(request):
    if request.user.role != 'RECEPTIONIST':
        raise PermissionDenied

    doctors = Doctor.objects.select_related(
        'department'
    ).all().order_by('name')

    context = {
        'doctors': doctors,
        'today': timezone.localdate(),
    }
    return render(request, 'receptionist-doctors.html', context)


@login_required(login_url='user_management:staff-login')
def receptionist_patients(request):
    if request.user.role != 'RECEPTIONIST':
        raise PermissionDenied

    patient_appointments = Appointment.objects.select_related('doctor', 'department').order_by('-appointment_date', '-appointment_time')

    patients = PatientProfile.objects.select_related('user').prefetch_related(
        Prefetch(
            'user__appointments',
            queryset=patient_appointments
        )
    ).order_by('full_name')

    context = {
        'patients': patients,
        'today': timezone.localdate(),
    }
    return render(request, 'receptionist-patients.html', context)