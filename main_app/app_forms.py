import datetime

from django import forms

from main_app.models import Appointments


DEPARTMENT_CHOICES = {
    " ": " ",
    "Emergency": "Emergency",
    "Counselling": "Counselling",
    "Radiology": "Radiology",
    "Physiotherapy": "Physiotherapy",
    "Antenatal": "Antenatal",
    "Orthopedics": "Orthopedics",
    "Gynaecology": "Gynaecology",
    "Oncology": "Oncology",
    "Pathology": "Pathology"
}
APPOINTMENT_CHOICES = {
    ' ': ' ',
    'Consultation': 'Consultation',
    'Follow-up treatment': 'Follow-up treatment',
    'Diagnostic test': 'Diagnostic test'
}
TIME_CHOICES = {
    ' ': ' ',
    '9:00AM - 10:30AM': '9:00AM - 10:30AM',
    '11:00AM - 12:30PM': '11:00AM - 12:30PM',
    '2:00PM - 03:30PM': '2:00PM - 03:30PM'
}
class Appointment(forms.ModelForm):
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select)
    appointment_type = forms.ChoiceField(choices=APPOINTMENT_CHOICES, widget=forms.Select)
    appointment_time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select)
    class Meta:
        model = Appointments
        fields = ['age', 'appointment_date', 'appointment_time',
                  'appointment_type', 'department']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'max': datetime.date.today() + datetime.timedelta(days=7)}),
        }



class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)