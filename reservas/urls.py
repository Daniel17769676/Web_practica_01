from django.urls import path
from .views import (procesar_reserva_view, reserva_exito_view, obtener_servicios)

app_name = 'reservas'  # Namespace

urlpatterns = [

path('procesar-reserva/', procesar_reserva_view, name='procesar_reserva'),
path('reserva_exito/<int:reserva_id>', reserva_exito_view, name='reserva_exito'),
path('obtener-servicios/', obtener_servicios, name='obtener_servicios'),

]