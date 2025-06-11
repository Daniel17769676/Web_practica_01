from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import ReservaUsuarios
from servicios.models import Disponibilidad, ServicioDia  # Importa el modelo Disponibilidad desde servicios
from django.views.decorators.http import require_GET




# Vista para mostrar los servicios disponibles (GET)
def seleccionar_servicios_view (request):
    #Obtenemos solo los valores unicos del campo 'servicio' del modelo Disponibilidad
    servicios= Disponibilidad.objects.values_list('servicio', flat=True).distinct()
    #Obtenemos los dias unicos del modelo ServicioDia desde la BBDD
    dias= ServicioDia.objects.values_list('dia', flat=True).distinct()
    return render(request, 'reservas/reservar.html', {'servicios': servicios, 'dias': dias})

@require_GET  # Asegura que solo se acepten peticiones GET
def get_dias_por_servicio_view(request):
    servicio = request.GET.get('servicio')
    
    if not servicio:
        return JsonResponse({'error': 'Parámetro "servicio" requerido'}, status=400)
    
    try:
        # Consulta optimizada con select_related (si hay relaciones ForeignKey)
        dias = ServicioDia.objects.filter(
            disponibilidad__servicio__iexact=servicio  # iexact para ignorar mayúsculas/minúsculas
        ).values_list('dia', flat=True).distinct()
        
        # Obtener nombres legibles de los días
        dias_choices = dict(ServicioDia.OPCIONES_DIAS)
        dias_data = [
            {'value': dia, 'text': dias_choices.get(dia, dia.capitalize())} 
            for dia in dias
        ]
        
        return JsonResponse({'dias': dias_data})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



        
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


