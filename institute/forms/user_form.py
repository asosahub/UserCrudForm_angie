from django import forms
from institute.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Nuevo usuario: Obligatorio, Actualizar: Opcional"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age', 'email', 'career', 'rol', 'clubs']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'age': 'Age',
            'email': 'Email Address',
            'career': 'Career',
            'rol' : 'Rol',
            'clubs': 'Clubs',
        }
        widgets = {
            #crear clases para uso de bootstrap
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'career': forms.Select(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'clubs': forms.CheckboxSelectMultiple(),
        }
    
    def clean(self):
        cleaned_data = super().clean()

        first_name = cleaned_data.get('first_name', '').strip()
        last_name = cleaned_data.get('last_name', '').strip()
        age = cleaned_data.get('age', '')
        email = cleaned_data.get('email', '').strip().lower()
        rol = cleaned_data.get('rol', '')
        password = cleaned_data.get('password', '')

        #validacion nombre y apellido
        if not first_name:
            self.add_error('first_name', "El nombre no puede estar vacío")
        if not last_name:
            self.add_error('last_name', "El apellido no puede estar vacío")

        #validacion de edad
        if age is not None and age < 18:
            self.add_error('age', "La edad debe ser mayor o igual a 18")

        #validacion email
        if not email:
            self.add_error('email', "El email no puede estar vacío")
        else:
            # Verificar si el email ya existe
            instance = self.instance
            if instance and instance.pk:
                #para edicion: excluir el usuario actual
                if User.objects.filter(email__iexact=email).exclude(pk=instance.pk).exists():
                    self.add_error('email', "Ya existe un usuario con este email")
            else:
                #para creacion: verificar si existe
                if User.objects.filter(email__iexact=email).exists():
                    self.add_error('email', "Ya existe un usuario con este email")

        #validacion email
        if not rol:
            self.add_error('email', "El email no puede estar vacío")

        # Validación contraseña (solo obligatoria si es creación)
        if not self.instance.pk and not password:
            self.add_error('password', "La contraseña es obligatoria para nuevos usuarios")

        return cleaned_data