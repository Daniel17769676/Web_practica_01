from django.urls import path
from usuarios.views import cancelar_reserva, confirmar_reserva, login_administrador, panel_administrador, logout_administrador, generar_reportes


app_name = 'usuarios'  # Namespace

urlpatterns = [
    path('administrador/login/', login_administrador, name='login_administrador'),
    path('panel-administrador/', panel_administrador, name='panel_administrador'),
    path('administrador/logout/', logout_administrador, name='logout_administrador'),
    path('cancelar/<int:reserva_id>/', cancelar_reserva, name='cancelar_reserva'),
    path('confirmar/<int:reserva_id>/', confirmar_reserva, name='confirmar_reserva'),
    path('reportes/generar/', generar_reportes, name='generar_reportes'),
]
