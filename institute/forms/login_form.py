from django import forms
from institute.models import User

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
        )
    password = forms.CharField(
        label='Contraseña', 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )