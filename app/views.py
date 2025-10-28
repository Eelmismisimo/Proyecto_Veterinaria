from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django import forms
from .models import Mascota, Dueño
from .forms import MascotaForm, CitaForm
from datetime import date
from .models import Cita, Veterinario, Consulta 
from .forms import ConsultaForm 


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
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def cita_crear(request):
    if not (tiene_rol(request.user, 'REC') or tiene_rol(request.user, 'ADM')):
        messages.error(request, 'Acceso denegado. Solo la Recepcionista puede agendar citas.')
        return redirect('dashboard')
    form = CitaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        nueva_cita = form.save(commit=False)
        if not nueva_cita.estado:
             nueva_cita.estado = 'PRO' 
        try:
            nueva_cita.full_clean() 
            nueva_cita.save()
            messages.success(request, 'Cita agendada con éxito. Disponibilidad y superposición validadas.')
            return redirect('cita_listado')
        except ValidationError as e:
            form.add_error(None, e)
            messages.error(request, 'Error de validación al agendar la cita. Verifique horario y disponibilidad del veterinario.')
    return render(request, 'cita/form.html', {'form': form, 'titulo': 'Agendar Nueva Cita'})
# ----------------------------------------------------------------------
def cita_modificar(request, id):
    if not (tiene_rol(request.user, 'REC') or tiene_rol(request.user, 'ADM')):
        messages.error(request, 'Acceso denegado. Solo la Recepcionista puede modificar citas.')
        return redirect('dashboard')
    cita = get_object_or_404(Cita, id=id)
    form = CitaForm(request.POST or None, instance=cita)
    if request.method == 'POST' and form.is_valid():
        cita_modificada = form.save(commit=False)
        try:
            cita_modificada.full_clean() 
            cita_modificada.save()
            messages.success(request, 'Cita modificada con éxito.')
            return redirect('cita_listado')
        except ValidationError as e:
            form.add_error(None, e)
            messages.error(request, 'Error de validación al modificar la cita.')
    return render(request, 'cita/form.html', {'form': form, 'titulo': f'Modificar Cita ID: {cita.id}'})
# ----------------------------------------------------------------------
def cita_cancelar(request, id):
    if not (tiene_rol(request.user, 'REC') or tiene_rol(request.user, 'ADM')):
        messages.error(request, 'Acceso denegado. Solo la Recepcionista puede cancelar citas.')
        return redirect('dashboard')
    cita = get_object_or_404(Cita, id=id)
    if request.method == 'POST':
        if cita.estado != 'COM': 
            cita.estado = 'CAN' 
            cita.save()
            messages.warning(request, f'Cita de {cita.mascota.nombre} cancelada.')
        else:
            messages.error(request, 'No se puede cancelar una cita que ya fue completada.')   
        return redirect('cita_listado')
    return render(request, 'cita/confirm_cancel.html', {'cita': cita})
# ----------------------------------------------------------------------
def cita_listado(request):
    citas = Cita.objects.all().select_related('mascota', 'veterinario')
    if tiene_rol(request.user, 'VET'):
        try:
            veterinario_actual = Veterinario.objects.get(user=request.user)
            citas = citas.filter(veterinario=veterinario_actual).order_by('fecha_hora')
        except Veterinario.DoesNotExist:
            citas = Cita.objects.none()
            messages.warning(request, 'Su perfil de veterinario no está completo.')
    elif tiene_rol(request.user, 'CLI'):
        try:
            cliente_actual = Cliente.objects.get(user=request.user)
            citas = citas.filter(mascota__dueño=cliente_actual).order_by('fecha_hora')
        except Cliente.DoesNotExist:
            citas = Cita.objects.none()
            messages.warning(request, 'Su perfil de cliente no está completo.')
    return render(request, 'cita/lista.html', {'citas': citas})
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def citas_del_dia(request):
    if not (tiene_rol(request.user, 'VET') or tiene_rol(request.user, 'ADM')):
        messages.error(request, 'Acceso denegado. Solo Veterinarios pueden ver esta agenda.')
        return redirect('dashboard')
    today = timezone.now().date()
    citas = Cita.objects.filter(fecha_hora__date=today).order_by('fecha_hora')
    if tiene_rol(request.user, 'VET'):
        try:
            veterinario_actual = Veterinario.objects.get(user=request.user)
            citas = citas.filter(veterinario=veterinario_actual)
        except Veterinario.DoesNotExist:
            citas = Cita.objects.none()
            messages.error(request, 'Perfil de Veterinario no encontrado.')
    citas_pendientes = citas.filter(estado='PRO').exclude(consulta__isnull=False)
    context = {
        'citas': citas_pendientes,
        'hoy': today,
        'titulo': 'Citas Pendientes del Día',
    }
    return render(request, 'consulta/agenda_dia.html', context) 
  # ----------------------------------------------------------------------
def registrar_consulta(request, cita_id):
    if not (tiene_rol(request.user, 'VET') or tiene_rol(request.user, 'ADM')):
        messages.error(request, 'Acceso denegado. Solo Veterinarios pueden registrar consultas.')
        return redirect('dashboard')
    cita = get_object_or_404(Cita, id=cita_id)
    if tiene_rol(request.user, 'VET'):
        try:
            veterinario_actual = Veterinario.objects.get(user=request.user)
            if cita.veterinario != veterinario_actual:
                messages.error(request, 'Solo puede registrar consultas de sus citas asignadas.')
                return redirect('citas_del_dia')
        except Veterinario.DoesNotExist:
            messages.error(request, 'Perfil de Veterinario no encontrado.')
            return redirect('dashboard')
    if hasattr(cita, 'consulta'):
        messages.warning(request, 'Esta cita ya tiene una consulta médica registrada.')
        return redirect('citas_del_dia')
    form = ConsultaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        consulta = form.save(commit=False)
        consulta.cita = cita 
        try:
            consulta.full_clean() 
            consulta.save()
            cita.estado = 'COM'
            cita.save()
            messages.success(request, f'Consulta y diagnóstico registrados para {cita.mascota.nombre}. Cita marcada como completada.')
            return redirect('historial_mascota', mascota_id=cita.mascota.id)
        except ValidationError as e:
            form.add_error(None, e) 
            messages.error(request, 'Error de validación al registrar la consulta.')
    context = {
        'form': form,
        'cita': cita,
        'titulo': f'Registrar Consulta para {cita.mascota.nombre}',
    }
    return render(request, 'consulta/registrar_consulta.html', context) #
