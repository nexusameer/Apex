from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from datetime import datetime
from .models import *

class IndexView(TemplateView):
    template_name = 'index.html'


class ContactView(TemplateView):
    template_name = 'contact.html'

class AboutView(TemplateView):
    template_name = 'about.html'

class DoctorView(TemplateView):
    template_name = 'doctors.html'

class TermsView(TemplateView):
    template_name = 'Terms.html'

class ServiceView(TemplateView):
    template_name = 'services.html'

class ErrorView(TemplateView):
    template_name = '404.html'

class AppointmentView(TemplateView):
    template_name = 'appointment.html'


def create_patient(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        patient = Patient.objects.create(
            first_name=first_name,
            last_name=last_name
        )
        return redirect('create_profile', patient_id=patient.id)
    
    return render(request, 'create_patient.html')

def create_profile(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    profile_image = request.FILES.get('profile_image')
    if profile_image and profile_image.size > 1024 * 1024:
        return render(request, 'create_profile.html', {
            'patient': patient,
            'error': 'Image file must be under 1MB.'
        })

    if request.method == 'POST':
        # Parse DOB safely
        raw_dob = request.POST.get('policy_holder_dob')
        policy_holder_dob = None
        if raw_dob:
            try:
                policy_holder_dob = datetime.strptime(raw_dob, '%Y-%m-%d').date()
            except ValueError:
                return render(request, 'create_profile.html', {
                    'patient': patient,
                    'error': 'Invalid date format for Policy Holder DOB. Use YYYY-MM-DD.'
                })

        profile = PatientProfile.objects.create(
            user=patient,
            dob=request.POST.get('dob'),
            birth_sex=request.POST.get('birth_sex'),
            gender_identity=request.POST.get('gender_identity'),
            email=request.POST.get('email'),
            primary_phone=request.POST.get('primary_phone'),
            address=request.POST.get('address'),
            po_box=request.POST.get('po_box'),
            emergency_contact_name=request.POST.get('emergency_contact_name'),
            emergency_contact_phone=request.POST.get('emergency_contact_phone'),
            insurance_id=request.POST.get('insurance_id'),
            insurance_company=request.POST.get('insurance_company'),
            policy_group=request.POST.get('policy_group'),
            policy_holder_name=request.POST.get('policy_holder_name'),
            policy_holder_relationship=request.POST.get('policy_holder_relationship'),
            policy_holder_dob=policy_holder_dob,
            policy_holder_address=request.POST.get('policy_holder_address'),
            policy_holder_phone=request.POST.get('policy_holder_phone'),
            profile_image=profile_image
        )

        return redirect('select_services', username=patient.username)

    return render(request, 'create_profile.html', {'patient': patient})


def select_services(request, username):
    patient = get_object_or_404(Patient, username=username)
    services = Service.objects.all()

    if request.method == 'POST':
        selected_service_ids = [
            int(key.split('_')[1]) for key in request.POST if key.startswith('service_')
        ]

        patient_profile = patient.patientprofile
        patient_profile.services.set(selected_service_ids)  # Replaces old services with new
        patient_profile.save()

        return redirect('error')  # or redirect to next step like 'signature'

    return render(request, 'select_services.html', {
        'patient': patient,
        'services': services
    })



