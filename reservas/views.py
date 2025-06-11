from django.shortcuts import render, redirect
from .models import ReservaUsuarios
from servicios.models import Disponibilidad, ServicioDia  # Importa el modelo Disponibilidad desde servicios


# Vista para mostrar los servicios disponibles (GET)
def seleccionar_servicios_view (request):
    #Obtenemos solo los valores unicos del campo 'servicio' del modelo Disponibilidad
    servicios= Disponibilidad.objects.values_list('servicio', flat=True).distinct()
    #Obtenemos los dias unicos del modelo ServicioDia desde la BBDD
    dias= ServicioDia.objects.values_list('dia', flat=True).distinct()
    return render(request, 'reservas/reservar.html', {'servicios': servicios, 'dias': dias})

        
# Vista para procesar la reserva (POST)
def procesar_reserva_view(request):
    if request.method == 'POST':
        #obtener los datos del formulario
        servicio = request.POST.get('servicio')
        dia = request.POST.get('dia')
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        observaciones = request.POST.get('observaciones') 

        # Guardar los datos del formulario en la base de datos  
        reserva = Reserva(
            servicio=servicio,
            dia=dia,
            horario=horario,
            nombre_cliente=nombre,
            telefono=telefono,
            email=email,
            observaciones=observaciones
        )
        reserva.save()

        return redirect('reservas:reserva_exito')  # Redirige a la plantilla de confirmación
    return render(request, 'reservas/reservar.html') 


def reserva_exito_view(request):
    # Renderiza la plantilla de confirmación de reserva exitosa
    return render(request, 'reservas/reserva_exito.html')


