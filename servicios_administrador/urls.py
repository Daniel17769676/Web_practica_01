from django.urls import path
from .views import disponibilidad_view, confirmacion_adm_view

app_name = 'servicios_administrador'

urlpatterns = [
  path('disponibilidad/', disponibilidad_view, name='disponibilidad_view'),
  path('confirmacion/', confirmacion_adm_view, name='confirmacion_adm_view'),

]