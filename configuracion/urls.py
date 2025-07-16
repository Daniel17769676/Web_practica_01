from django.contrib import admin
from django.urls import path, include
from configuracion import views 
from reservas.views import reservar_servicios_view, procesar_reserva_view, get_dias_por_servicio_view, get_horarios, reserva_exito_view
from servicios.views import disponibilidad_view


urlpatterns = [
    path('admin/', admin.site.urls),  # URL para el panel de administración
    path('', views.base, name='base'),  # URL para la página de inicio
    path('servicios/', include('servicios.urls')),
    path('reservas/', include(('reservas.urls', 'reservas'), namespace='reservas')),  # Incluye las URLs de la aplicación reservas
    path('usuarios/', include('usuarios.urls')),  # Incluye las URLs de la aplicación usuarios


    #URLs de reservas
    path('reservas/reservar/', reservar_servicios_view, name='reservar'),
    path('reservas/procesar-reserva/', procesar_reserva_view, name='procesar_reserva'),
    path('reservas/get-dias/', get_dias_por_servicio_view, name='get_dias'),
    path('reservas/get-horarios/', get_horarios, name='get_horarios'),
    path('reservas/reserva_exito/', reserva_exito_view, name='reserva_exito'),
    
    #URLs de servicios
    path('disponibilidad/', disponibilidad_view, name='disponibilidad'),   

    #URLs de usuarios
    
    
  
]
