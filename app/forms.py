from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import Cliente, UsuarioEx

class FormRegistroEx(UserCreationForm):
    class Meta:
        model = UsuarioEx
        fields = ['username', 'email', 'password1', 'password2', 'rut', 'telefono', 'tipo_Usuario']

class FormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields ='__all__'

