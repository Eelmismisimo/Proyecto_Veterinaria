from django.urls import path
from urls.py import views 
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('mascotas/', views.mascota_listado, name='mascota_listado'),
    path('mascotas/crear/', views.mascota_crear, name='mascota_crear'),
    path('mascotas/editar/<int:id>/', views.mascota_editar, name='mascota_editar'),
    
]
