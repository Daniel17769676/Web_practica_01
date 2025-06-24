from django.urls import path
from. import views
from .views import get_dias_por_servicio_view

app_name = 'reservas'  # Namespace

urlpatterns = [
#Muestra el formularios con los servicios disponibles desde la base de datos (GET)
path('seleccionar_servicios/', views.seleccionar_servicios_view, name='mostrar_servicios'),

#Procesa el formulario de reserva (POST) y redirige a la vista de confirmación
path('reservar/procesar/', views.procesar_reserva_view, name='reservar_procesar'),

#Redirige a la vista de confirmación de reserva exitosa
path('reserva_exito/', views.reserva_exito_view, name='reserva_exito'),

#Vista para obtener los dias disponibles por servicio (GET)
path('get_dias_por_servicio/', get_dias_por_servicio_view, name='get_dias_por_servicio'),

#Vista para obtener los horarios disponibles por servicio y día (GET)
path('get_horarios/', views.get_horarios, name='get_horarios'),

]