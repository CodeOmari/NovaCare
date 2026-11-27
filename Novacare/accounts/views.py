from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.contrib import messages
from datetime import datetime

from .models import Appointment, Consultation, Prescription, LaboratoryResult, Invoice, Payment
from main_app.models import Department, Doctor
from django.utils.dateparse import parse_date
from decimal import Decimal

@login_required(login_url='user_management:patient-login')
def patient_dashboard(request):
    patient = request.user.patient_profile

    upcoming_appointments = Appointment.objects.select_related('doctor', 'department', 'patient', 'patient__patient_profile').filter(patient=request.user,
        appointment_date__gte=timezone.localdate(),
        status__in=['PENDING', 'APPROVED']).order_by('appointment_date', 'appointment_time')

    active_prescriptions = Prescription.objects.filter(consultation__appointment__patient=request.user,status='ACTIVE').count()

    context = {
        'patient': patient,
        'upcoming_appointments': upcoming_appointments,
        'active_prescriptions': active_prescriptions,
        'next_appointment': upcoming_appointments.first(),
        'total_appointments': Appointment.objects.filter(patient=request.user).count(),
    }
    return render(request, 'patient-dashboard.html', context)


@login_required(login_url='user_management:patient-login')
def patient_appointments(request):
    if request.user.role != 'PATIENT':
        raise PermissionDenied

    patient = request.user.patient_profile
    active_statuses = ['PENDING', 'APPROVED']

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'book':
            department_id = request.POST.get('department')
            doctor_id = request.POST.get('doctor')
            appointment_date = request.POST.get('preferred_date')
            appointment_time = request.POST.get('appointment_time')
            reason = request.POST.get('reason', '').strip()

            try:
                department = Department.objects.get(id=department_id)
                doctor = Doctor.objects.get(id=doctor_id, department=department, is_available=True)
                selected_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
                selected_time = datetime.strptime(appointment_time, '%H:%M').time()

                available_days = [
                    day.strip()[:3].lower()
                    for day in doctor.availability.split(',')
                ]

                selected_weekday = selected_date.strftime('%a').lower()

                selected_datetime = timezone.make_aware(datetime.combine(selected_date, selected_time), timezone.get_current_timezone())

                if selected_datetime <= timezone.now():
                    messages.error(request, 'Please select a future date and time.')

                elif selected_weekday not in available_days:
                    messages.error(request, f'This doctor is only available on {doctor.availability}.')

                elif not reason:
                    messages.error(request, 'Please provide a reason for your appointment.')

                elif Appointment.objects.filter(doctor=doctor, appointment_date=selected_date, appointment_time=selected_time, status__in=active_statuses).exists():
                    messages.error(request, 'This doctor already has an appointment scheduled for that date and time. Please choose another time.')

                else:
                    Appointment.objects.create(
                        patient=request.user, department=department, doctor=doctor, appointment_date=selected_date, appointment_time=selected_time, reason=reason,)

                    messages.success(request, 'Your appointment request has been submitted successfully.')
                    return redirect('accounts:patient-appointments')

            except (Department.DoesNotExist, Doctor.DoesNotExist):
                messages.error(request, 'The selected department or doctor is invalid or unavailable.')

            except (ValueError, TypeError, AttributeError):
                messages.error(request, 'Please provide valid appointment details.')

        elif action == 'reschedule':
            appointment_id = request.POST.get('appointment_id')
            new_date = request.POST.get('preferred_date')
            new_time = request.POST.get('appointment_time')

            try:
                appointment = Appointment.objects.select_related('doctor').get(id=appointment_id, patient=request.user)

                if appointment.status not in active_statuses:
                    messages.error(request, 'This appointment cannot be rescheduled.')

                else:
                    selected_date = datetime.strptime(new_date, '%Y-%m-%d').date()

                    selected_time = datetime.strptime(new_time, '%H:%M').time()

                    available_days = [
                        day.strip()[:3].lower()
                        for day in doctor.availability.split(',')
                    ]

                    selected_weekday = selected_date.strftime('%a').lower()

                    selected_datetime = timezone.make_aware(datetime.combine(selected_date, selected_time),
                        timezone.get_current_timezone())

                    if selected_datetime <= timezone.now():
                        messages.error(request, 'Please select a future date and time.')

                    elif selected_weekday not in available_days:
                        messages.error(request, f'This doctor is only available on {appointment.doctor.availability}.')

                    elif Appointment.objects.filter(doctor=appointment.doctor, appointment_date=selected_date,
                        appointment_time=selected_time, status__in=active_statuses).exclude(id=appointment.id).exists():
                        messages.error(request, 'This doctor already has an appointment scheduled for that date and time. Please choose another time.')

                    else:
                        appointment.appointment_date = selected_date
                        appointment.appointment_time = selected_time
                        appointment.save()

                        messages.success(request, 'Your appointment has been rescheduled successfully.')
                        return redirect('accounts:patient-appointments')

            except Appointment.DoesNotExist:
                messages.error(request, 'Appointment not found or you do not have permission to modify it.')

            except (ValueError, TypeError, AttributeError):
                messages.error(request, 'Please provide valid appointment details.')

        elif action == 'cancel':
            appointment_id = request.POST.get('appointment_id')

            try:
                appointment = Appointment.objects.get(id=appointment_id, patient=request.user)

                if appointment.status != 'PENDING':
                    messages.error(request, 'Only pending appointments can be cancelled. Approved appointments cannot be cancelled.')

                else:
                    appointment_datetime = timezone.make_aware(
                        datetime.combine(appointment.appointment_date, appointment.appointment_time), timezone.get_current_timezone()
                    )

                    if appointment_datetime <= timezone.now():
                        messages.error(request, 'Past appointments cannot be cancelled.')

                    else:
                        appointment.status = 'CANCELLED'
                        appointment.save(update_fields=['status', 'updated_at'])

                        messages.success(request, 'Your appointment has been cancelled successfully.')
                        return redirect('accounts:patient-appointments')

            except Appointment.DoesNotExist:
                messages.error(request, 'Appointment not found or you do not have permission to cancel it.')

    appointments = Appointment.objects.filter(patient=request.user).select_related('department', 'doctor')

    current_time = timezone.now()

    for appointment in appointments:
        appointment_datetime = timezone.make_aware(
            datetime.combine(appointment.appointment_date, appointment.appointment_time),timezone.get_current_timezone())
        appointment.is_upcoming = appointment_datetime >= current_time
    return render(request, 'patient-appointments.html', {'patient': patient, 'appointments': appointments, 'departments': Department.objects.all(), 'doctors': Doctor.objects.filter(is_available=True),})


@login_required(login_url='user_management:patient-login')
def medical_records(request):
    patient = request.user.patient_profile

    consultations = Consultation.objects.select_related('appointment', 'appointment__doctor', 'appointment__department',).filter(
        appointment__patient=request.user, status='COMPLETED').order_by('-date')

    context = {
        'patient': patient,
        'consultations': consultations,
        'today': timezone.localdate(),
    }
    return render(request, 'patient-medical-records.html', context)


@login_required(login_url='user_management:patient-login')
def patient_prescriptions(request):
    prescriptions = Prescription.objects.select_related('consultation', 'consultation__appointment', 'consultation__appointment__doctor','consultation__appointment__department',).filter(
        consultation__appointment__patient=request.user).order_by('-prescribed_date', '-created_at')

    context = {
        'patient': request.user.patient_profile,
        'prescriptions': prescriptions,
    }
    return render(request, 'patient-prescriptions.html', context)


@login_required(login_url='user_management:patient-login')
def patient_laboratory_results(request):
    lab_results = LaboratoryResult.objects.select_related(
        'consultation',
        'consultation__appointment',
        'consultation__appointment__doctor',
        'consultation__appointment__department',
    ).filter(
        consultation__appointment__patient=request.user
    ).order_by('-requested_date', '-created_at')

    context = {
        'patient': request.user.patient_profile,
        'lab_results': lab_results,
    }
    return render(request, 'patient-laboratory-results.html', context)


@login_required(login_url='user_management:patient-login')
def patient_billing(request):
    invoices = Invoice.objects.filter(patient=request.user).prefetch_related('payments').order_by('-date', '-created_at')

    payment_history = Payment.objects.filter(invoice__patient=request.user,status='SUCCESSFUL').select_related('invoice').order_by('-date', '-created_at')

    outstanding_balance = Decimal('0.00')
    unpaid_count = 0

    for invoice in invoices:
        outstanding_balance += invoice.amount_due

        if invoice.amount_due > 0 and invoice.status != 'CANCELLED':
            unpaid_count += 1

    context = {
        'patient': request.user.patient_profile,
        'invoices': invoices,
        'payment_history': payment_history,
        'outstanding_balance': outstanding_balance,
        'unpaid_count': unpaid_count,
    }

    return render(request, 'patient-billing.html', context)