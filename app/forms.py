from django import forms
from django.contrib.auth.forms import UserCreationForm
from models import UsuarioEx, Cliente , Cita
from .models import Mascota
from .models import Consulta

class FormRegistroEx(UserCreationForm):
    class Meta:
        model = UsuarioEx
        fields = ['username', 'email', 'password1', 'password2', 'rut', 'telefono', 'tipo_Usuario']

class FormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields ='__all__'

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

class ConsultaForm(forms.ModelForm): #
    class Meta:
        model = Consulta
        fields = ['diagnostico', 'tratamiento_prescrito', 'medicamentos', 'proxima_cita', 'costo_consulta']
        widgets = {
            'diagnostico': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'tratamiento_prescrito': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'medicamentos': forms.TextInput(attrs={'class': 'form-control'}),
            'proxima_cita': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'costo_consulta': forms.NumberInput(attrs={'class': 'form-control'}),
        }
