from django.urls import path
from .views import GestionDisponibilidadView, ListaDisponibilidadView, disponibilidad_view

app_name = 'servicios_administrador'

urlpatterns = [
 path('nueva-disponibilidad/', GestionDisponibilidadView.as_view(), name='nueva_disponibilidad'),
 path('disponibilidad/', disponibilidad_view, name='disponibilidad_view'),

]