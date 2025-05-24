from django.shortcuts import render, redirect
from .models import Disponibilidad
from django.contrib import messages


# Vista para CREAR disponibilidades (ADMINISTRADOR)  
def disponibilidad_view(request):
    if request.method == 'POST':
        print("DATOS RECIBIDOS:", request.POST) #Imprime los datos recibidos en la consola para depuración.
        #Guardar los datos del formulario en la base de datos
        Disponibilidad.objects.create(
            administrador=request.POST['administrador'],
            dia=request.POST['dia'],
            hora_inicio=request.POST['hora_inicio'],
            hora_fin=request.POST['hora_fin'],
            servicio=request.POST['servicio'],
            disponible=True # esta linea guarda el valor de la casilla de verificación y lo convierte en un booleano, un booleano es un tipo de dato que solo puede tener dos valores: verdadero o falso.
            )             
        return redirect('servicios_administrador:confirmacion') #Redirect es una función que redirige al usuario a otra URL después de que se haya procesado el formulario. En este caso, redirige a la plantilla 'Confirmacion.html' después de guardar la disponibilidad en la base de datos.
    return render(request, 'mi_web/Disponibilidad.html')#En caso de que la solicitud no sea un POST, se renderiza la plantilla 'Disponibilidad.html' para mostrar el formulario al usuario.

# Vista para confirmar datos guardados al ofrecer disponibilidad (ADMINISTRADOR)
def confirmacion_view(request):
    return render(request, 'mi_web/Confirmacion.html')