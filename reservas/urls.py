from django.urls import path
from .views import (reservar_servicios_view, procesar_reserva_view, reserva_exito_view)

app_name = 'reservas'  # Namespace

urlpatterns = [

path('procesar-reserva/', procesar_reserva_view, name='procesar_reserva'),
path('reserva_exito/<int:reserva_id>', reserva_exito_view, name='reserva_exito'),
path('reservar/', reservar_servicios_view, name='reservar'),

]