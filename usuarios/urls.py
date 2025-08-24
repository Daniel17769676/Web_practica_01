from django.urls import path
from usuarios.views import login_administrador, panel_administrador


app_name = 'usuarios'  # Namespace

urlpatterns = [
    path('administrador/login/', login_administrador, name='login_administrador'),
    path('panel-administrador/', panel_administrador, name='panel_administrador'),
  
]    