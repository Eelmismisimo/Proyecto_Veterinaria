from django.contrib.auth.forms import UserCreationForm
from models import UsuarioEx

class FormRegistroEx(UserCreationForm):
    class Meta:
        model = UsuarioEx
        fields = ['username', 'email', 'password1', 'password2', 'rut', 'telefono', 'tipo_usuario']
