from django import forms 
from institute.models import Career

class CareerForm(forms.ModelForm):
    class Meta: 
        model = Career
        fields = ['name']
        labels = {
            'name': 'Career Name'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '').strip()
    
        if not name:
            self.add_error('name', "El nombre no puede estar vacío")
        else:
            # Verificar si el nombre ya existe
            instance = self.instance
            if instance and instance.pk:
                #para edicion: excluir la carrera actual
                if Career.objects.filter(name__iexact=name).exclude(pk=instance.pk).exists():
                    self.add_error('name', "Ya existe una carrera con este nombre")
            else:
                #para creacion: verificar si existe
                if Career.objects.filter(name__iexact=name).exists():
                    self.add_error('name', "Ya existe una carrera con este nombre")
    
        return cleaned_data