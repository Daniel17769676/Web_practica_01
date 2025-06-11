from django.urls import path
from .views import disponibilidad_view, confirmacion_view

app_name = 'servicios'

urlpatterns = [
  path('disponibilidad/', disponibilidad_view, name='disponibilidad'),
  path('confirmacion/', confirmacion_view, name='confirmacion'),

]