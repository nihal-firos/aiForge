# users/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegistrationForm(forms.ModelForm):
    # Define fields for the form
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    role = forms.ChoiceField(
        choices=Profile.USER_ROLE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        # Check that the email is unique
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email