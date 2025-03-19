"""
URL configuration for proyecto_web01 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mi_web import views


urlpatterns = [
    path('', views.Portada, name='portada'), #indicamos que la página de inicio es la página Portada con los signos de comillas vacíos ''
    path('admin/', admin.site.urls),     
    path('reservas/', views.reservas_view, name='reservas'),
    path('reserva/confirmacion/<int:reserva_id>', views.reserva_confirmacion_view, name='reserva_confirmacion'),
    
]
