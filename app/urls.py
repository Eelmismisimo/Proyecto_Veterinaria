from django.urls import path
from urls.py import views 
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('mascotas/', views.mascota_listado, name='mascota_listado'),
    path('mascotas/crear/', views.mascota_crear, name='mascota_crear'),
    path('mascotas/editar/<int:id>/', views.mascota_editar, name='mascota_editar'),
    path('mascotas/eliminar/<int:id>/', views.mascota_eliminar, name='mascota_eliminar'),

    path('citas/', views.cita_listado, name='cita_listado'),
    path('citas/agendar/', views.cita_crear, name='cita_crear'), 
    path('citas/modificar/<int:id>/', views.cita_modificar, name='cita_modificar'), 
    path('citas/cancelar/<int:id>/', views.cita_cancelar, name='cita_cancelar'),

    path('citas/hoy/', views.citas_del_dia, name='citas_del_dia'), 
    path('consulta/registrar/<int:cita_id>/', views.registrar_consulta, name='registrar_consulta'), 
    path('historial/mascota/<int:mascota_id>/', views.historial_mascota, name='historial_mascota'),
]
