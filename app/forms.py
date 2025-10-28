from django.contrib.auth.forms import UserCreationForm
from models import UsuarioEx
from .models import Mascota

class FormRegistroEx(UserCreationForm):
    class Meta:
        model = UsuarioEx
        fields = ['username', 'email', 'password1', 'password2', 'rut', 'telefono', 'tipo_usuario']

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'dueño', 'especie', 'raza', 'fecha_nacimiento', 'sexo', 'color', 'estado']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'sexo': forms.Select(choices=[('macho', 'macho'), ('hembra', 'hembra')]),
            'estado': forms.Select(choices=[('activo', 'activo'), ('inactivo', 'inactivo')]),
        }

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['mascota', 'veterinario', 'fecha_hora', 'motivo_consulta', 'estado', 'observaciones']
        widgets = {
            'mascota': forms.Select(attrs={'class': 'form-select'}),
            'veterinario': forms.Select(attrs={'class': 'form-select'}),
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}), 
            'motivo_consulta': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
