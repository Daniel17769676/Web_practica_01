from django.urls import path
from .views import (panel_reservas_view, procesar_reserva_view, reserva_exito_view, obtener_servicios, obtener_horarios_reservados)

app_name = 'reservas'  # Namespace

urlpatterns = [

path('procesar-reserva/', procesar_reserva_view, name='procesar_reserva'),
path('reserva_exito/<int:reserva_id>', reserva_exito_view, name='reserva_exito'),
path('obtener-servicios/', obtener_servicios, name='obtener_servicios'), #Pagina principal de reservas
path('horarios-reservados/', obtener_horarios_reservados, name='horarios_reservados'),
path('panel-reservas/', panel_reservas_view, name='panel_reservas'),

]