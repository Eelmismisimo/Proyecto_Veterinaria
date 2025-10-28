from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django import forms
from .models import Mascota, Dueño
from .forms import MascotaForm

def tiene_rol(user, rol_code):
    if not user.is_authenticated:
        return False
    if rol_code == 'ADM':
        return user.is_superuser
    if rol_code == 'REC':
        return user.is_staff and not user.is_superuser
    if rol_code == 'CLI':
        return not user.is_staff and not user.is_superuser
    return False
def dashboard(request):
    return render(request, 'base.html', {})
# ----------------------------------------------------------------------
def mascota_listado(request):
    mascotas = Mascota.objects.all()
    if tiene_rol(request.user, 'CLI'):
        try:
            mascotas = mascotas.filter(dueño=request.user.cliente) 
        except Cliente.DoesNotExist:
            mascotas = Mascota.objects.none()
            messages.warning(request, 'Su perfil de cliente no está completo.')
    return render(request, 'mascota/lista.html', {'mascotas': mascotas})
    # ----------------------------------------------------------------------
def mascota_crear(request):
    if not (tiene_rol(request.user, 'CLI') or tiene_rol(request.user, 'REC') or tiene_rol(request.user, 'ADM')):
        messages.error(request, 'Acceso denegado.')
        return redirect('dashboard')
    form = MascotaForm(request.POST or None)
    cliente_actual = None
    if tiene_rol(request.user, 'CLI'):
        try:
            cliente_actual = Cliente.objects.get(user=request.user)
            form.fields['dueño'].initial = cliente_actual
            form.fields['dueño'].widget = forms.HiddenInput()
        except Cliente.DoesNotExist:
            messages.error(request, 'Error: Perfil de cliente no encontrado.')
            return redirect('dashboard')
    if request.method == 'POST' and form.is_valid():
        nueva_mascota = form.save(commit=False)
        if tiene_rol(request.user, 'CLI'):
            nueva_mascota.dueño = cliente_actual 
        try:
            nueva_mascota.full_clean() 
            nueva_mascota.save()
            messages.success(request, f'Mascota "{nueva_mascota.nombre}" registrada con éxito.')
            return redirect('mascota_listado')
        except ValidationError as e:
            form.add_error(None, e) 
            messages.error(request, 'Error de validación al guardar.')
    return render(request, 'mascota/form.html', {'form': form, 'titulo': 'Registrar Mascota'})
    # ----------------------------------------------------------------------
def mascota_editar(request, id):
    if tiene_rol(request.user, 'CLI'):
        mascota = get_object_or_404(Mascota, id=id, dueño=request.user.cliente)
    elif tiene_rol(request.user, 'REC') or tiene_rol(request.user, 'ADM'):
        mascota = get_object_or_404(Mascota, id=id)
    else:
        messages.error(request, 'Acceso denegado.')
        return redirect('dashboard')
    form = MascotaForm(request.POST or None, instance=mascota)
    if tiene_rol(request.user, 'CLI'):
        form.fields['dueño'].widget = forms.HiddenInput()
    if request.method == 'POST' and form.is_valid():
        mascota_editada = form.save(commit=False)
        try:
            mascota_editada.full_clean()
            mascota_editada.save()
            messages.success(request, f'Mascota "{mascota_editada.nombre}" actualizada con éxito.')
            return redirect('mascota_listado')
        except ValidationError as e:
            form.add_error(None, e)
            messages.error(request, 'Error de validación al actualizar.')
    return render(request, 'mascota/form.html', {'form': form, 'titulo': f'Editar Mascota: {mascota.nombre}'})
    # ----------------------------------------------------------------------
def mascota_eliminar(request, id):
    if tiene_rol(request.user, 'CLI'):
        mascota = get_object_or_404(Mascota, id=id, dueño=request.user.cliente)
    elif tiene_rol(request.user, 'REC') or tiene_rol(request.user, 'ADM'):
        mascota = get_object_or_404(Mascota, id=id)
    else:
        messages.error(request, 'Acceso denegado.')
        return redirect('dashboard')
    if request.method == 'POST':
        nombre = mascota.nombre
        mascota.delete()
        messages.success(request, f'Mascota "{nombre}" eliminada correctamente.')
        return redirect('mascota_listado')
    return render(request, 'mascota/confirm_delete.html', {'mascota': mascota})
