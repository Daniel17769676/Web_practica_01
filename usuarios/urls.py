from django.urls import path
from .views import ReservaView, ReservaExitoView

app_name = 'usuarios'  # Namespace

urlpatterns = [
path('reservar/', ReservaView.as_view(), name='reservar'),
path('reserva-exito/', ReservaExitoView.as_view(), name='reserva_exito'),

]