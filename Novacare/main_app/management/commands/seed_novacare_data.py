from django.core.management.base import BaseCommand
from main_app.models import Department, Doctor, DepartmentService

class Command(BaseCommand):
    help = 'Populate NovaCare departments and doctor profiles'

    def handle(self, *args, **kwargs):
        departments = [
            {
                'name': 'General Medicine',
                'slug': 'general-medicine',
                'description': (
                    'Primary care, diagnosis and treatment for adults.'
                ),
                'service_one': 'General consultations',
                'service_two': 'Chronic disease management',
                'service_three': 'Health screening',
                'service_four': 'Vaccinations',
            },
            {
                'name': 'Pediatrics',
                'slug': 'pediatrics',
                'description': (
                    'Child-friendly care from newborns to teens.'
                ),
                'service_one': 'Well-baby clinic',
                'service_two': 'Immunizations',
                'service_three': 'Growth monitoring',
                'service_four': 'Pediatric emergencies',
            },
            {
                'name': 'Cardiology',
                'slug': 'cardiology',
                'description': (
                    'Heart health, diagnostics and long-term care.'
                ),
                'service_one': 'ECG & echocardiography',
                'service_two': 'Stress testing',
                'service_three': 'Hypertension clinic',
                'service_four': 'Cardiac rehabilitation'
            },
            {
                'name': 'Dermatology',
                'slug': 'dermatology',
                'description': (
                    'Skin, hair and nail conditions.'
                ),
                'service_one': 'Acne & eczema care',
                'service_two': 'Skin cancer screening',
                'service_three': 'Allergy testing',
                'service_four': 'Minor procedures',
            },
            {
                'name': 'Gynecology',
                'slug': 'gynecology',
                'description': (
                    "Women's health and maternity care."
                ),
                'service_one': 'Antenatal care',
                'service_two': 'Family planning',
                'service_three': 'Cervical screening',
                'service_four': 'Menopause clinic',
            },
            {
                'name': 'Orthopedics',
                'slug': 'orthopedics',
                'description': (
                    'Bones, joints, muscles and sports injuries.'
                ),
                'service_one': 'Fracture care',
                'service_two': 'Joint replacement',
                'service_three': 'Sports medicine',
                'service_four': 'Physiotherapy',
            },
            {
                'name': 'Dentistry',
                'slug': 'dentistry',
                'description': (
                    'Preventive, restorative and cosmetic dental care.'
                ),
                'service_one': 'Check-ups & cleaning',
                'service_two': 'Fillings & root canal',
                'service_three': 'Orthodontics',
                'service_four': 'Teeth whitening',
            },
            {
                'name': 'Radiology',
                'slug': 'radiology',
                'description': (
                    'Imaging and diagnostic services.'
                ),
                'service_one': 'Digital X-ray',
                'service_two': 'Ultrasound',
                'service_three': 'CT scan',
                'service_four': 'MRI',
            },
        ]

        for department_data in departments:
            department, created = Department.objects.update_or_create(
                slug=department_data['slug'],
                defaults=department_data
            )

            action = 'Created' if created else 'Updated'
            self.stdout.write(
                f'{action} department: {department.name}'
            )

        department_services = {
            'general-medicine': [
                'General consultations',
                'Chronic disease management',
                'Health screening',
                'Vaccinations',
            ],

            'pediatrics': [
                'Well-baby clinic',
                'Immunizations',
                'Growth monitoring',
                'Pediatric emergencies',
            ],

            'cardiology': [
                'ECG & echocardiography',
                'Stress testing',
                'Hypertension clinic',
                'Cardiac rehabilitation',
            ],

            'dermatology': [
                'Acne & eczema care',
                'Skin cancer screening',
                'Allergy testing',
                'Minor procedures',
            ],

            'gynecology': [
                'Antenatal care',
                'Family planning',
                'Cervical screening',
                'Menopause clinic',
            ],

            'orthopedics': [
                'Fracture care',
                'Joint replacement',
                'Sports medicine',
                'Physiotherapy',
            ],

            'dentistry': [
                'Check-ups & cleaning',
                'Fillings & root canal',
                'Orthodontics',
                'Teeth whitening',
            ],

            'radiology': [
                'Digital X-ray',
                'Ultrasound',
                'CT scan',
                'MRI',
            ],
        }

        for department_slug, services in department_services.items():
            department = Department.objects.get(slug=department_slug)

            for index, service_name in enumerate(services, start=1):
                DepartmentService.objects.update_or_create(
                    department=department,
                    name=service_name,
                    defaults={
                        'order': index
                    }
                )

        self.stdout.write(
            self.style.SUCCESS('Department services populated successfully.')
        )

        doctors = [
            {
                'name': 'Dr. Sarah Mwangi',
                'department': 'general-medicine',
                'role': 'General Physician',
                'qualification': 'MBChB, MMed (Internal Medicine)',
                'experience': 12,
                'availability': 'Monday, Tuesday, Thursday, Friday',
                'rating': 4.9,
                'about': (
                    'Experienced in preventive healthcare and '
                    'chronic disease management.'
                ),
                'slug': 'sarah-mwangi',
                'image': 'images/doctor-1.jpg',
            },
            {
                'name': 'Dr. David Thompson',
                'department': 'cardiology',
                'role': 'Cardiologist',
                'qualification': 'MD, FACC',
                'experience': 18,
                'availability': 'Monday, Wednesday, Friday',
                'rating': 4.8,
                'about': (
                    'Specializes in interventional cardiology '
                    'and heart failure management.'
                ),
                'slug': 'david-thompson',
                'image': 'images/doctor-2.jpg',
            },
            {
                'name': 'Dr. Priya Nair',
                'department': 'pediatrics',
                'role': 'Pediatrician',
                'qualification': 'MBBS, DCH, MD (Pediatrics)',
                'experience': 8,
                'availability': 'Tuesday, Wednesday, Thursday, Saturday',
                'rating': 4.9,
                'about': (
                    'Focuses on child development and family-centered care.'
                ),
                'slug': 'priya-nair',
                'image': 'images/doctor-3.jpg',
            },
            {
                'name': 'Dr. Kevin Lee',
                'department': 'dentistry',
                'role': 'Dental Surgeon',
                'qualification': 'BDS, MDS',
                'experience': 6,
                'availability': 'Monday, Wednesday, Friday, Saturday',
                'rating': 4.9,
                'about': (
                    'Provides gentle, modern dental care with an emphasis '
                    'on preventive treatment.'
                ),
                'slug': 'kevin-lee',
                'image': 'images/doctor-4.jpg',
            },
            {
                'name': 'Dr. Emily Carter',
                'department': 'dermatology',
                'role': 'Dermatologist',
                'qualification': 'MD, FAAD',
                'experience': 10,
                'availability': 'Wednesday, Thursday, Friday',
                'rating': 4.8,
                'about': (
                    'Specializes in skin conditions and skin cancer screening.'
                ),
                'slug': 'emily-carter',
                'image': 'images/doctor-5.jpg',
            },
            {
                'name': 'Dr. Samuel Okoye',
                'department': 'orthopedics',
                'role': 'Orthopedic Surgeon',
                'qualification': 'MBBS, FRCS (Ortho)',
                'experience': 22,
                'availability': 'Monday, Tuesday, Thursday',
                'rating': 4.7,
                'about': (
                    'Specializes in joint replacement and trauma surgery.'
                ),
                'slug': 'samuel-okoye',
                'image': 'images/doctor-6.jpg',
            },
            {
                'name': 'Dr. Grace Wanjiku',
                'department': 'gynecology',
                'role': 'Gynecologist',
                'qualification': 'MBChB, MMed (Obstetrics and Gynecology)',
                'experience': 10,
                'availability': 'Mon, Tue, Thu, Fri',
                'rating': 4.8,
                'about': 'Experienced in women’s health, reproductive healthcare, antenatal care and gynecological treatment.',
                'slug': 'grace-wanjiku',
                'image': 'images/doctor-7.png',
            },
            {
                'name': 'Dr. Michael Ochieng',
                'department': 'radiology',
                'role': 'Radiologist',
                'qualification': 'MBChB, MMed (Diagnostic Radiology)',
                'experience': 9,
                'availability': 'Mon, Wed, Thu, Sat',
                'rating': 4.7,
                'about': 'Experienced in medical imaging, diagnostic interpretation and supporting accurate clinical diagnosis.',
                'slug': 'michael-ochieng',
                'image': 'images/doctor-8.png',
            },
        ]

        for doctor_data in doctors:
            department_slug = doctor_data.pop('department')

            department = Department.objects.get(
                slug=department_slug
            )

            doctor, created = Doctor.objects.update_or_create(
                slug=doctor_data['slug'],
                defaults={
                    **doctor_data,
                    'department': department,
                }
            )

            action = 'Created' if created else 'Updated'
            self.stdout.write(
                f'{action} doctor: {doctor.name}'
            )

        self.stdout.write(
            self.style.SUCCESS(
                'NovaCare departments and doctors populated successfully!'
            )
        )