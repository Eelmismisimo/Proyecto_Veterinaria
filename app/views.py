from datetime import date
from django.shortcuts import render,redirect
from app.forms import FormCliente, FormRegistroEx
from django.contrib.auth import login,authenticate
from app.models import Cliente, Dueño

#:)
def test(request):
    return render(request, 'base.html')
def crear_usuario(request):
    if request.method == 'GET':
        form = FormRegistroEx()
    elif request.method == 'POST':
        form = FormRegistroEx(request.POST)
        if form.is_valid():
            user = form.save()
            if user.tipo_Usuario == 'Cliente':
                Cliente.objects.create(
                    usuario=user,
                    nombre_completo= request.POST.get("nombreCompleto"),  
                    direccion= request.POST.get("direccion"),  
                    telefono_contacto=user.telefono,
                    email=user.email,
                    fecha_registro= date.today()   
                    )
            login(request,user)
            return redirect("dashboard_cliente")
    return render(request, "Cliente_model/registro_usuario.html", {'form':form})


def IniciarSesion(request):
    if request.method == 'GET':
        return render(request, 'Cliente_model/login.html')
    elif request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password= password)
        if user :
            login(request, user)
            return redirect("dashboard_cliente")
        else:
            return render(request, "Cliente_model/login.html", {"error": "Credenciales incorrectas"})
    

def dashboard_cliente(request):
    return render(request, "Cliente_model/dashboard.html")

def autorizacion(request):
    if request.method == 'GET':
        return render(request, 'Dueño_model/Super_user.html')
    elif request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password= password)
        if user:
            if user.is_superuser:
                return redirect('adminReg')
            else:
                return render(request, "Dueño_model/login.html", {"error": "No tienes permisos de superusuario:("})
        else:
            return render(request, "Dueño_model/login.html", {"error": "Credenciales incorrectas"})

def adminreg(request):
    if request.method == 'GET':
        form = FormRegistroEx()
    elif request.method == 'POST':
        form = FormRegistroEx(request.POST)
        if form.is_valid():
            user = form.save()
            if user.tipo_Usuario == 'Administrador':
                Dueño.objects.create(
                    usuario=user,
                    nombre_completo= request.POST.get("nombreCompleto"),  
                    direccion= request.POST.get("direccion"),  
                    telefono_contacto=user.telefono,
                    email=user.email,
                    fecha_registro= date.today()   
                    )
            login(request,user)
            return redirect("dashboard_admin")
    return render(request, "Dueño_model/create.html", {'form':form})

def AdminLog(request):
    if request.method == 'GET':
        return render(request, 'Dueño_model/login.html')
    elif request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password= password)
        if user :
            if user.tipo_Usuario == 'Administrador':
                login(request, user)
                return redirect("adminDash")
            else:
                 return render(request, "Dueño_model/login.html", {"error": "No tienes permisos de Administrador:("})
        else:
            return render(request, "Dueño_model/login.html", {"error": "Credenciales incorrectas"})

def adminDash(request):

    return render(request, "Dueño_model/dashboard.html")

def listaClientes(request):
    clientes = Cliente.objects.all()
    data = {'clientes': clientes}
    return render(request, "Dueño_model/lista_clientes.html", data)

def EliminarCliente(request,id):
    cliente = Cliente.objects.get(id=id)
    cliente.delete()
    return redirect("listaClientes")

def ActualizarCliente(request,id):
    cliente = Cliente.objects.get(id=id)
    form = FormCliente(instance = cliente)
    if request.method =='POST':
        form = FormCliente(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
        return listaClientes(request)
    data = {'form': form}
    return render(request, 'Dueño_model/actualizar.html',data)
