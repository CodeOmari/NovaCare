from django import forms

from main_app.models import ChildPatient, AdultPatient

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
        widgets = {
            'phone_number': forms.TextInput(attrs={'type': 'number'}),
        }

ADULT_CHOICES = {"Male": "Male", "Female": "Female"}
class AdultForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=ADULT_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = AdultPatient
        fields = ['first_name', 'last_name', 'gender','phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'type': 'number'}),
        }