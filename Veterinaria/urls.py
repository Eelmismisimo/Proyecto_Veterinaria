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
    path('EliminarCliente/<int:id>',v.EliminarCliente, name="EliminarCliente"),

    path('mascotas/', v.mascota_listado, name='mascota_listado'),
    path('mascotas/crear/', v.mascota_crear, name='mascota_crear'),
    path('mascotas/editar/<int:id>/', v.mascota_editar, name='mascota_editar'),
    path('mascotas/eliminar/<int:id>/', v.mascota_eliminar, name='mascota_eliminar'),

    path('citas/', v.cita_listado, name='cita_listado'),
    path('citas/agendar/', v.cita_crear, name='cita_crear'), 
    path('citas/modificar/<int:id>/', v.cita_modificar, name='cita_modificar'), 
    path('citas/cancelar/<int:id>/', v.cita_cancelar, name='cita_cancelar'),

    path('citas/hoy/', v.citas_del_dia, name='citas_del_dia'), 
    path('consulta/registrar/<int:cita_id>/', v.registrar_consulta, name='registrar_consulta'), 
    path('historial/mascota/<int:mascota_id>/', v.historial_mascota, name='historial_mascota'),


]
