from .models import Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
from django.core.exceptions import ValidationError

COMMON_PASSWORD = {"123", "ciao"}


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=10)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, label = "Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label = "Confirm Password")
  


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if password1 != password2:
            raise ValidationError("Password not matching")

        if any(info.lower() in password1.lower() for info in [username, email]):
            raise ValidationError(
                "Your password can't be too similar to your other personal information.")

        if len(password1) < 8:
            raise ValidationError(
                "Your password must contain at least 8 characters.")

        if password1.lower() in COMMON_PASSWORD:
            raise ValidationError(
                "Your password can't be a commonly used password.")

        if password1.isnumeric():
            raise ValidationError("Your password can't be entirely numeric.")

        if not re.search(r"[A-Za-z]", password1):
            raise ValidationError(
                "Your password must contain at least one letter.")

        return cleaned_data
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

    


# users/forms.py


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture','Profile']


