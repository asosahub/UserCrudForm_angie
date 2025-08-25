from django import forms
from institute.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age', 'email']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'age': 'Age',
            'email': 'Email Address'
        }
        widgets = {
            #crear clases para uso de bootstrap
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
    def clean_age(self):
        #validacion de edad
        age = self.cleaned_data.get('age')
        if age is not None and age < 18:
            raise forms.ValidationError("El usuario debe ser mayor de edad")
        return age

    def save(self, commit=True):
        if self.instance.pk:
            # Actualizar usuario existente
            user = super().save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.age = self.cleaned_data['age']
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user
        else:
            # Crear nuevo usuario
            return super().save(commit=commit)