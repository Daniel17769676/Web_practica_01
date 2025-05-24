from django.shortcuts import render, redirect
from .models import ReservaUsuarios

def ReservaUsuarios(request):
    if request.method == 'POST':
        print("DATOS RECIBIDOS:", request.POST)
        # Guardar los datos del formulario en la base de datos
        ReservaUsuarios.objects.create(
            administrador_id=request.POST['administrador'],
            disponibilidad_id=request.POST['disponibilidad'],
            nombre=request.POST['nombre'],
            email=request.POST['email'],
            telefono=request.POST['telefono']
        )

        return redirect('usuarios:reserva_confirmacion')  # Redirige a la plantilla de confirmación
    return render(request, 'usuarios/reservar.html') 


