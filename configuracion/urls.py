from django.contrib import admin
from django.urls import path, include
from configuracion import views 
from reservas.views import obtener_servicios, procesar_reserva_view, reserva_exito_view
from servicios.views import disponibilidad_view


urlpatterns = [
    path('admin/', admin.site.urls),  # URL para el panel de administración
    path('', views.base, name='base'),  # URL para la página de inicio
    path('servicios/', include('servicios.urls')),
    path('reservas/', include(('reservas.urls', 'reservas'), namespace='reservas')),  # Incluye las URLs de la aplicación reservas
    path('usuarios/', include('usuarios.urls')),  # Incluye las URLs de la aplicación usuarios


    #URLs de reservas
    path('reservas/reservar/', obtener_servicios, name='obtener_servicios'),
    path('reservas/procesar-reserva/', procesar_reserva_view, name='procesar_reserva'),    
    path('reservas/reserva_exito/', reserva_exito_view, name='reserva_exito'),
    
    #URLs de servicios
    path('disponibilidad/', disponibilidad_view, name='disponibilidad'),   

    #URLs de usuarios
    path('usuarios/', include('usuarios.urls')),

]
