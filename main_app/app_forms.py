import datetime

from django import forms

from main_app.models import ChildPatient, AdultPatient, AdultAppointments

GENDER_CHOICES = {"Male": "Male", "Female": "Female"}
RELATIONSHIP_CHOICES = {"Father": "Father", "Mother": "Mother", "Sibling": "Sibling", "Relative": "Relative",
                        "Guardian": "Guardian"}
class ChildForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    parent_gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    relationship = forms.ChoiceField(choices=RELATIONSHIP_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = ChildPatient
        fields = ['first_name', 'last_name', 'gender','parent_first_name',
                  'parent_last_name', 'parent_gender', 'parent_phone_number',
                  'relationship']


ADULT_CHOICES = {"Male": "Male", "Female": "Female"}
class AdultForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=ADULT_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = AdultPatient
        fields = ['first_name', 'last_name', 'gender','phone_number']


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
class AdultAppointment(forms.ModelForm):
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select)
    appointment_type = forms.ChoiceField(choices=APPOINTMENT_CHOICES, widget=forms.Select)
    appointment_time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select)
    class Meta:
        model = AdultAppointments
        fields = ['age', 'appointment_date', 'appointment_time',
                  'appointment_type', 'department']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'max': datetime.date.today() + datetime.timedelta(days=7)}),
        }



class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)