from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from main_app.models import Doctor
from accounts.models import (
    Appointment, PatientProfile, Consultation,Prescription, Invoice, Payment, NursePatientAssignment, Admission, 
    NursingTask, VitalSign, Ward,)
from django.db.models import Prefetch, OuterRef, Subquery
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.db.models import Q, Count
from django.utils.dateparse import parse_date
from django.db.models import Sum
from decimal import Decimal
from django.http import JsonResponse

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
            today = timezone.localdate()

            if appointment.status != 'APPROVED':
                messages.error(request, 'Only approved appointments can be checked in.')

            elif appointment.appointment_date != today:
                messages.error(request, 'Patients can only be checked in on their scheduled appointment date.')

            elif appointment.checked_in:
                messages.info(request, 'This patient has already checked in.')

            else:
                appointment.checked_in = True
                appointment.save(update_fields=['checked_in', 'updated_at'])

                messages.success(request, 'Patient successfully checked in.')

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
        '-appointment_date', '-appointment_time', '-created_at')

    patients = PatientProfile.objects.filter(user__appointments__doctor=doctor).annotate(
        latest_appointment_status=Subquery(latest_appointment.values('status')[:1])).select_related(
        'user').prefetch_related(
        Prefetch('user__appointments', queryset=Appointment.objects.filter(doctor=doctor
            ).select_related('doctor').order_by('-appointment_date', '-appointment_time', '-created_at'),
            to_attr='doctor_appointments')).distinct().order_by('full_name')

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

    patient = get_object_or_404(PatientProfile.objects.filter(user__appointments__doctor=doctor).distinct(),pk=patient_id)

    appointments = Appointment.objects.filter(patient=patient.user, doctor=doctor).select_related('department').order_by('-appointment_date','-appointment_time')

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

    today = timezone.localdate()

    appointments = Appointment.objects.select_related('patient', 'patient__patient_profile', 'department', 'doctor').filter(status='APPROVED')

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')

        appointment = get_object_or_404(Appointment, id=appointment_id, status='APPROVED')

        if appointment.appointment_date > today:
            messages.error(request, 'You cannot check in a patient before their appointment date.')

        elif appointment.appointment_date < today:
            messages.error(request, 'This appointment date has already passed.')

        elif appointment.checked_in:
            messages.info(request, 'This patient has already checked in.')

        else:
            appointment.checked_in = True
            appointment.save(update_fields=['checked_in', 'updated_at'])

            messages.success(request, 'Patient successfully checked in.')
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
            Q(patient__patient_profile__full_name__icontains=search_query) | Q(doctor__name__icontains=search_query) |
            Q(department__name__icontains=search_query))

    doctors = Doctor.objects.all().order_by('name')

    context = {
        'appointments': appointments,
        'selected_date': selected_date,
        'selected_doctor': selected_doctor,
        'search_query': search_query,
        'doctors': doctors,
        'today': today,
    }
    return render(request, 'receptionist-appointments.html', context)


@login_required(login_url='user_management:staff-login')
def receptionist_dashboard(request):
    if request.user.role != 'RECEPTIONIST':
        raise PermissionDenied

    today = timezone.localdate()

    todays_appointments = (Appointment.objects.select_related('patient', 'patient__patient_profile', 'doctor','department').filter(appointment_date=today).order_by('appointment_time'))

    recent_patients = (PatientProfile.objects.select_related('user').prefetch_related(
            Prefetch('user__appointments',
                queryset=Appointment.objects.select_related('doctor').order_by(
                    '-appointment_date', '-appointment_time'),to_attr='recent_appointments')).order_by('-created_at')[:4])

    context = {
        'today': today,
        'total_patients': PatientProfile.objects.count(),
        'todays_appointments_count': todays_appointments.count(),
        'pending_appointments_count': Appointment.objects.filter(status='PENDING').count(),
        'recently_registered_count': PatientProfile.objects.filter(created_at__date=today).count(),
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
        'assigned_patients_count': doctor_appointments.values('patient').distinct().count(),
        'todays_appointments_count': todays_appointments.count(),
        'pending_consultations_count': doctor_appointments.filter(status='PENDING').count(),
        'completed_consultations_count': doctor_appointments.filter(status='COMPLETED').count(),
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
        'appointment','appointment__patient','appointment__patient__patient_profile','appointment__doctor',
        'appointment__department').filter(appointment__doctor=doctor)
    
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

    doctors = Doctor.objects.select_related('department').all().order_by('name')

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
        Prefetch('user__appointments', queryset=patient_appointments)).order_by('full_name')

    context = {
        'patients': patients,
        'today': timezone.localdate(),
    }
    return render(request, 'receptionist-patients.html', context)


@login_required(login_url='user_management:staff-login')
def new_consultation(request):
    if request.user.role != 'DOCTOR':
        raise PermissionDenied

    doctor = request.user.doctor_profile
    today = timezone.localdate()

    eligible_appointments = Appointment.objects.select_related(
        'patient', 'patient__patient_profile', 'doctor','department',
    ).filter(doctor=doctor, appointment_date=today, status='APPROVED',
    ).exclude(consultation__isnull=False).order_by('appointment_time')

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment')

        appointment = get_object_or_404(eligible_appointments, id=appointment_id)

        symptoms = request.POST.get('symptoms', '').strip()
        examination_notes = request.POST.get('examination_notes', '').strip()
        diagnosis = request.POST.get('diagnosis', '').strip()
        treatment_plan = request.POST.get('treatment_plan', '').strip()
        follow_up_value = request.POST.get('follow_up_date', '').strip()
        follow_up_date = parse_date(follow_up_value) if follow_up_value else None

        if follow_up_value and follow_up_date is None:
            messages.error(request, 'Please enter a valid follow-up date.')
            return render(request, 'new-consultation.html', {'doctor': doctor, 'appointments': eligible_appointments, 'today': today, })

        if not diagnosis or not treatment_plan:
            messages.error(request, 'Please provide both a diagnosis and treatment plan.')
        else:
            Consultation.objects.create(appointment=appointment, symptoms=symptoms, examination_notes=examination_notes, diagnosis=diagnosis,
                treatment_plan=treatment_plan, follow_up_date=follow_up_date, status='COMPLETED',)

            messages.success(request, 'Consultation successfully recorded.')
            return redirect('staff:doctor-consultations')

    context = {
        'doctor': doctor,
        'appointments': eligible_appointments,
        'today': today,
    }
    return render(request, 'new-consultation.html', context)

@login_required(login_url='user_management:staff-login')
def doctor_consultation_detail(request, consultation_id):
    if request.user.role != 'DOCTOR':
        raise PermissionDenied

    doctor = request.user.doctor_profile

    consultation = get_object_or_404(
        Consultation.objects.select_related(
            'appointment','appointment__patient','appointment__patient__patient_profile',
            'appointment__doctor','appointment__department',).prefetch_related('prescriptions'),
        id=consultation_id,appointment__doctor=doctor,)

    context = {
        'doctor': doctor,
        'consultation': consultation,
        'prescriptions': consultation.prescriptions.all(),
    }
    return render(request, 'doctor-consultation-detail.html', context)


@login_required(login_url='user_management:staff-login')
def edit_consultation(request, consultation_id):
    if request.user.role != 'DOCTOR':
        raise PermissionDenied

    doctor = request.user.doctor_profile

    consultation = get_object_or_404(Consultation, id=consultation_id, appointment__doctor=doctor,)

    if request.method == 'POST':
        symptoms = request.POST.get('symptoms', '').strip()
        examination_notes = request.POST.get('examination_notes', '').strip()
        diagnosis = request.POST.get('diagnosis', '').strip()
        treatment_plan = request.POST.get('treatment_plan', '').strip()
        follow_up_value = request.POST.get('follow_up_date', '').strip()

        follow_up_date = (parse_date(follow_up_value)
            if follow_up_value else None
        )

        if follow_up_value and follow_up_date is None:
            messages.error(request, 'Please enter a valid follow-up date.')

        elif not diagnosis or not treatment_plan or not examination_notes:
            messages.error(request, 'Please complete the examination notes, diagnosis and treatment plan.')

        else:
            consultation.symptoms = symptoms
            consultation.examination_notes = examination_notes
            consultation.diagnosis = diagnosis
            consultation.treatment_plan = treatment_plan
            consultation.follow_up_date = follow_up_date

            consultation.save()

            messages.success(request, 'Consultation details successfully updated.')

            return redirect('staff:doctor-consultation-detail', consultation_id=consultation.id)

    context = {'doctor': doctor, 'consultation': consultation,}
    return render(request, 'edit-consultation.html', context)


@login_required(login_url='user_management:staff-login')
def issue_prescription(request, consultation_id):
    if request.user.role != 'DOCTOR':
        raise PermissionDenied

    doctor = request.user.doctor_profile

    consultation = get_object_or_404(
        Consultation.objects.select_related('appointment', 'appointment__patient', 'appointment__patient__patient_profile',
            'appointment__doctor',), id=consultation_id, appointment__doctor=doctor,)

    if request.method == 'POST':
        medication_name = request.POST.get('medication_name', '').strip()
        quantity_value = request.POST.get('quantity', '').strip()
        dosage_frequency = request.POST.get('dosage_frequency', '').strip()
        duration_value = request.POST.get('duration_days', '').strip()
        instructions = request.POST.get('instructions', '').strip()

        if not medication_name or not dosage_frequency:
            messages.error(request, 'Please provide the medicine name and dosage.')

        elif not quantity_value.isdigit() or int(quantity_value) < 1:
            messages.error(request, 'Enter a valid medicine quantity.')

        elif not duration_value.isdigit() or int(duration_value) < 1:
            messages.error(request, 'Enter a valid prescription duration.')

        else:
            today = timezone.localdate()
            duration_days = int(duration_value)

            Prescription.objects.create(consultation=consultation, medication_name=medication_name,
                quantity=int(quantity_value), dosage_frequency=dosage_frequency,
                duration_days=duration_days, start_date=today, end_date=today + timedelta(days=duration_days - 1), prescribed_date=today,
                instructions=instructions,)

            messages.success(request, f'{medication_name} successfully added to the prescription.')
            return redirect('staff:doctor-consultation-detail', consultation_id=consultation.id)

    context = {
        'doctor': doctor,
        'consultation': consultation,
        'prescriptions': consultation.prescriptions.all(),
    }
    return render(request, 'issue-prescription.html', context)


@login_required(login_url='user_management:staff-login')
def accountant_dashboard(request):
    if request.user.role != 'ACCOUNTANT':
        raise PermissionDenied

    invoices = Invoice.objects.exclude(
        status='CANCELLED').select_related('patient').prefetch_related('payments').order_by('-date', '-created_at')

    total_invoiced = invoices.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')

    payments_received = Payment.objects.filter(
        status='SUCCESSFUL',invoice__status__in=['PENDING', 'PARTIALLY_PAID', 'PAID', 'OVERDUE']
    ).aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')

    outstanding_balance = sum((invoice.amount_due for invoice in invoices), Decimal('0.00'))

    pending_invoices = invoices.filter(status='PENDING').count()

    outstanding_invoices = [
        invoice for invoice in invoices
        if invoice.amount_due > Decimal('0.00')
    ][:5]

    recent_payments = Payment.objects.filter(status='SUCCESSFUL').select_related('invoice','invoice__patient').order_by('-date', '-created_at')[:5]

    context = {
        'total_invoiced': total_invoiced,
        'payments_received': payments_received,
        'outstanding_balance': outstanding_balance,
        'pending_invoices': pending_invoices,
        'outstanding_invoices': outstanding_invoices,
        'recent_payments': recent_payments,
        'today': timezone.localdate(),
    }
    return render(request, 'accountant-dashboard.html', context)


@login_required(login_url='user_management:staff-login')
def nurse_dashboard(request):
    if request.user.role != 'NURSE':
        raise PermissionDenied

    today = timezone.localdate()

    assignments = NursePatientAssignment.objects.filter(nurse=request.user, is_active=True
    ).select_related('patient', 'patient__patient_profile')

    assigned_patients = assignments.count()

    patient_ids = assignments.values_list('patient_id', flat=True)

    current_admissions = Admission.objects.filter(
        patient_id__in=patient_ids, status='ADMITTED').select_related('patient','patient__patient_profile', 'ward')

    todays_tasks = NursingTask.objects.filter(
        nurse=request.user, scheduled_date=today
    ).select_related('patient', 'patient__patient_profile').order_by('scheduled_time')

    attention_tasks = NursingTask.objects.filter(nurse=request.user, priority__in=['HIGH', 'URGENT']).exclude(status__in=['COMPLETED', 'CANCELLED'])

    recent_vitals = VitalSign.objects.filter(
        nurse=request.user).select_related('patient','patient__patient_profile').order_by('-recorded_at')[:5]

    context = {
        'assigned_patients': assigned_patients,
        'current_admissions': current_admissions.count(),
        'attention_count': attention_tasks.count(),
        'todays_tasks_count': todays_tasks.count(),
        'todays_tasks': todays_tasks,
        'recent_vitals': recent_vitals,
        'today': today,
    }
    return render(request, 'nurse-dashboard.html', context)


@login_required(login_url='user_management:staff-login')
def nurse_patients(request):
    if request.user.role != 'NURSE':
        raise PermissionDenied

    search_query = request.GET.get('search', '').strip()

    assignments = NursePatientAssignment.objects.filter(
        nurse=request.user, is_active=True).select_related('patient', 'patient__patient_profile').order_by('-assigned_at')

    if search_query:
        assignments = assignments.filter(
            Q(patient__email__icontains=search_query) |
            Q(patient__patient_profile__full_name__icontains=search_query) |
            Q(patient__patient_profile__phone__icontains=search_query)
        )

    context = {
        'assignments': assignments,
        'search_query': search_query,
        'total_patients': assignments.count(),
    }
    return render(request, 'nurse-patients.html', context)


@login_required(login_url='user_management:staff-login')
def nurse_manager_dashboard(request):
    if request.user.role != 'NURSE MANAGER':
        raise PermissionDenied

    today = timezone.localdate()

    total_nurses = request.user.__class__.objects.filter(role='NURSE', is_active=True).count()

    active_assignments = NursePatientAssignment.objects.filter(is_active=True)

    assigned_patients = active_assignments.values('patient').distinct().count()

    unassigned_patients = PatientProfile.objects.exclude(user_id__in=active_assignments.values('patient_id')).count()

    current_admissions = Admission.objects.filter(status='ADMITTED').count()

    ward_occupancy = Ward.objects.filter(is_active=True
    ).annotate(occupied_beds=Count('admissions', filter=Q(admissions__status='ADMITTED'))
    ).order_by('name')

    for ward in ward_occupancy:
        ward.occupancy_percentage = (
            round((ward.occupied_beds / ward.capacity) * 100)
            if ward.capacity > 0 else 0)

    recent_assignments = NursePatientAssignment.objects.select_related(
        'nurse', 'patient', 'patient__patient_profile').order_by('-assigned_at')[:5]

    context = {
        'today': today,
        'total_nurses': total_nurses,
        'assigned_patients': assigned_patients,
        'unassigned_patients': unassigned_patients,
        'current_admissions': current_admissions,
        'ward_occupancy': ward_occupancy,
        'recent_assignments': recent_assignments,
    }
    return render(request, 'nurse-manager-dashboard.html', context)



@login_required(login_url='user_management:staff-login')
def nurse_manager_assignments(request):
    if request.user.role != 'NURSE MANAGER':
        raise PermissionDenied

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'assign':
            patient_id = request.POST.get('patient')
            nurse_id = request.POST.get('nurse')

            patient = get_object_or_404(PatientProfile.objects.select_related('user'), id=patient_id)

            nurse = get_object_or_404(request.user.__class__, id=nurse_id, role='NURSE', is_active=True)

            existing_assignment = NursePatientAssignment.objects.filter(patient=patient.user,
                nurse=nurse, is_active=True).exists()

            if existing_assignment:
                messages.warning(request, 'This nurse is already assigned to this patient.')
            else:
                NursePatientAssignment.objects.create(patient=patient.user, nurse=nurse)

                messages.success(request, f'{nurse.work_id} successfully assigned to {patient.full_name}.')

        elif action == 'deactivate':
            assignment_id = request.POST.get('assignment_id')

            assignment = get_object_or_404(NursePatientAssignment, id=assignment_id, is_active=True)

            assignment.is_active = False
            assignment.save(update_fields=['is_active'])

            messages.success(request, 'Nursing assignment successfully deactivated.')
        return redirect('staff:nurse-manager-assignments')

    search_query = request.GET.get('search', '').strip()
    selected_status = request.GET.get('status', 'ACTIVE').upper()

    patients = PatientProfile.objects.select_related('user').order_by('full_name')

    if search_query:
        patients = patients.filter(
            Q(full_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )

    nurses = request.user.__class__.objects.filter(role='NURSE', is_active=True).order_by('work_id')

    assignments = NursePatientAssignment.objects.select_related('nurse', 'patient', 'patient__patient_profile').order_by('-assigned_at')

    if selected_status == 'ACTIVE':
        assignments = assignments.filter(is_active=True)
    elif selected_status == 'INACTIVE':
        assignments = assignments.filter(is_active=False)
    else:
        selected_status = 'ALL'

    context = {
        'patients': patients,
        'nurses': nurses,
        'assignments': assignments,
        'search_query': search_query,
        'selected_status': selected_status,
        'today': timezone.localdate(),
    }

    return render(request, 'nurse-manager-assignments.html', context)


@login_required(login_url='user_management:staff-login')
def nurse_manager_search(request):
    if request.user.role != 'NURSE MANAGER':
        raise PermissionDenied

    search_type = request.GET.get('type', '')
    query = request.GET.get('q', '').strip()

    if len(query) < 2:
        return JsonResponse({'results': []})

    results = []

    if search_type == 'patient':
        patients = PatientProfile.objects.select_related('user').filter(
            full_name__icontains=query).order_by('full_name')[:10]

        results = [
            {
                'id': patient.id,
                'name': patient.full_name,
                'detail': f"Phone: {patient.phone or 'Not provided'}",
                'email': patient.user.email or 'No email provided',
            }
            for patient in patients
        ]

    elif search_type == 'nurse':
        nurses = request.user.__class__.objects.filter(role='NURSE', is_active=True, work_id__icontains=query).order_by('work_id')[:10]
        
        results = [
            {
                'id': nurse.id,
                'name': nurse.work_id,
                'detail': f"{nurse.first_name} {nurse.last_name}".strip() or 'Name not provided',
            }
            for nurse in nurses
        ]

    return JsonResponse({'results': results})