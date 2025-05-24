from django.urls import path
from .views import ReservaUsuarios

app_name = 'usuarios'  # Namespace

urlpatterns = [
path('reservar/', ReservaUsuarios, name='reservar'),

]