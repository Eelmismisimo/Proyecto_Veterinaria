from django.db import models
from django.contrib.auth.models import AbstractUser


class UsuarioEx(AbstractUser):
        rut = models.CharField(max_length=10, unique=True)
        telefono = models.IntegerField()
        tipo_Usuario = models.CharField(max_length=20, choices=[('Administrador','Administrador'),
                                                                ('Veterinario','Veterinario'),
                                                                ('Cliente','Cliente'),
                                                                ('Recepcionista','Recepcionista')])

class Cliente(models.Model):
        usuario= models.OneToOneField(UsuarioEx, on_delete=models.CASCADE)
        nombre_completo = models.CharField(max_length=50)
        direccion = models.CharField(max_length=50)
        telefono_contacto = models.IntegerField()
        email = models.EmailField()
        fecha_registro = models.DateField()

class Dueño(models.Model):
        usuario= models.OneToOneField(UsuarioEx, on_delete=models.CASCADE)
        nombre_completo = models.CharField(max_length=50)
        direccion = models.CharField(max_length=50)
        telefono_contacto = models.IntegerField()
        email = models.EmailField()
        fecha_registro = models.DateField()

class Veterinario(models.Model):
        usuario= models.OneToOneField(UsuarioEx, on_delete=models.CASCADE)
        nombre_completo = models.CharField(max_length=50)
        especialidad = models.CharField(max_length=50)
        licencia_profesional = models.ImageField()
        telefono = models.IntegerField()

class Mascota(models.Model):
        dueño = models.ForeignKey(Cliente, on_delete=models.CASCADE)
        nombre = models.CharField(max_length=20)
        especie = models.CharField(max_length=20)
        Raza = models.CharField(max_length=20)
        fecha_nacimiento = models.DateField()
        sexo = models.CharField( max_length=10 ,choices=[('hembra','hembra'),('macho','macho')])
        color = models.CharField(max_length=20)
        estado = models.BooleanField()

class Cita(models.Model):
        mascota = models.ForeignKey(Mascota,on_delete=models.CASCADE)
        veterinario = models.ForeignKey(Veterinario, on_delete=models.CASCADE)
        fecha = models.DateField()
        hora = models.TimeField()
        motivo_consulta = models.CharField(max_length=100)
        estado = models.CharField(max_length=50,choices=[('Programada','Programada'),('Completada','Completada'),('Cancelada','Cancelada')])
        observaciones = models.CharField(max_length=200)

class HistorialMedico(models.Model):
        cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
        fecha_consulta = models.DateField()
        diagnostico = models.CharField(max_length=100)
        tratamiento_prescrito = models.CharField(max_length=100)
        medicamentos = models.CharField(max_length=30)
        costo_consulta = models.IntegerField()
