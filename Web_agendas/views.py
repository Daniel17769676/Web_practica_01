from django.shortcuts import render
from servicios_administrador.models import Disponibilidad


# Creamos la vista home, que sirve para mostrar la página de inicio
def base(request):  
    return render(request, 'base.html') # Renderiza la plantilla base.html

def disponibilidad_view(request):
    return render(request, 'mi_web/Disponibilidad.html')


