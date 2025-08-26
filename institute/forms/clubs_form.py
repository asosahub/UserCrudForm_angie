from django import forms
from institute.models import Clubs

class ClubsForm(forms.ModelForm):
    class Meta:
        model = Clubs
        fields = ['name']
        labels = {
            'name': 'Club Name'
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
            # Verificar si ya existe un club con el mismo nombre
            instance = self.instance
            if instance and instance.pk:
                #para edicion: excluir el club actual
                if Clubs.objects.filter(name__iexact=name).exclude(pk=instance.pk).exists():
                    self.add_error('name', "Ya existe un club con este nombre")

            else:
                #para creacion: verificar si existe
                if Clubs.objects.filter(name__iexact=name).exists():
                    self.add_error('name', "Ya existe un club con ese nombre")

        return cleaned_data