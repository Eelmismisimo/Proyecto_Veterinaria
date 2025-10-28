from django.contrib.auth.decorators import login_required
from .models import mascota
from .forms import Mascota_model
"-------------------------------------------"
def lista_mascotas(request):
    mascotas = Mascota.objects.filter(dueño=request.user.cliente)
    return render(request, 'mascota/lista.html', {'mascotas': mascotas})

def crear_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.dueño = request.user.cliente
            mascota.save()
            return redirect('lista_mascotas')
    else:
        form = MascotaForm()
    return render(request, 'mascota/form.html', {'form': form})

def editar_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id, dueño=request.user.cliente)
    form = MascotaForm(request.POST or None, instance=mascota)
    if form.is_valid():
        form.save()
        return redirect('lista_mascotas')
    return render(request, 'mascota/form.html', {'form': form})
"------------------------------------------------------------------------------"
def eliminar_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id, dueño=request.user.cliente)
    mascota.delete()
    return redirect('lista_mascotas')
