from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from user_management.models import Details
from datetime import date


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='Enter your email address')


class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(label='New Password',
                                   widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}))
    confirm_password = forms.CharField(label='Confirm Password',
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password")
        password2 = cleaned_data.get("confirm_password")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data
    

GENDER_CHOICES = {
    "Male": "Male",
    "Female": "Female"
}
IDENTITY_CHOICES = {
    "ID": "ID",
    "Passport": "Passport",
    "Birth Certificate": "Birth Certificate"
}
class PersonalDetailsForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    identity_type = forms.ChoiceField(choices=IDENTITY_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Details
        fields = ['identity_type', 'identity_number', 'first_name', 'last_name', 'gender', 'dob', 'phone_number', 'profile_pic']
        # .isofformat ensure the input follows the YYYY-MM-DD format
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'min':'1935-01-01', 'max': date.today().isoformat()}),
            'identity_number': forms.TextInput(attrs={'placeholder': 'Enter ID, Passport, or Birth Certificate number' })
        }