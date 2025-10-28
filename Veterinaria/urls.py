from app import views as v
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.test),
    path('login/', v.IniciarSesion, name="loginUsuario"),
    path('registro/',v.crear_usuario, name='crearUsuario'),
    path('home_u/', v.dashboard_cliente, name='dashboard_cliente'),
    path('adminreg/', v.adminreg, name="adminReg"),
    path('adminlogin/', v.AdminLog, name="adminLogin"),
    path('adminDash/', v.adminDash, name='adminDash' ),
    path('autho/', v.autorizacion, name="autho"),
    path('listaClientes/', v.listaClientes, name="listaClientes"),
    path('ActualizarCliente/<int:id>', v.ActualizarCliente, name="ActualizarCliente"),
    path('EliminarCliente/<int:id>',v.EliminarCliente, name="EliminarCliente")


]
