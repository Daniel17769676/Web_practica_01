from django.contrib import admin
from django.urls import path, include
from Web_agendas import views


urlpatterns = [
    path('admin/', admin.site.urls),  # URL para el panel de administración
    path('', views.base, name='base'),  # URL para la página de inicio
    path('servicios/', include('servicios_administrador.urls')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),  # URL para la aplicación de usuarios
    path('disponibilidad/', views.disponibilidad_view, name='disponibilidad'),  # URL para la disponibilidad

   
]
