from django.urls import path
from .views import (get_dias_por_servicio_view, reservar_servicios_view, procesar_reserva_view, get_horarios, reserva_exito_view)

app_name = 'reservas'  # Namespace

urlpatterns = [

path('procesar-reserva/', procesar_reserva_view, name='procesar_reserva'),
path('get_dias_por_servicio/', get_dias_por_servicio_view, name='get_dias'),
path('get_horarios/', get_horarios, name='get_horarios'),
path('reserva_exito/<int:reserva_id>', reserva_exito_view, name='reserva_exito'),
path('reservar/', reservar_servicios_view, name='reservar'),

]