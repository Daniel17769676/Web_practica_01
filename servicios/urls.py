from django.urls import path
from .views import disponibilidad_view, confirmacion_view
from . import views

app_name = 'servicios'

urlpatterns = [
  
  path('disponibilidad/', disponibilidad_view, name='disponibilidad'),
  path('confirmacion/<int:disponibilidad_id>/', views.confirmacion_view, name='confirmacion'),
  

]