from django.contrib.auth.forms import UserCreationForm
from models import UsuarioEx
from .models import mascota.html

class FormRegistroEx(UserCreationForm):
    class Meta:
        model = UsuarioEx
        fields = ['username', 'email', 'password1', 'password2', 'rut', 'telefono', 'tipo_usuario']

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'sexo', 'color', 'estado']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'sexo': forms.Select(choices=[('macho', 'macho'), ('hembra', 'hembra')]),
            'estado': forms.Select(choices=[('activo', 'activo'), ('inactivo', 'inactivo')]),
        }
