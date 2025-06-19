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
    #Agregar la lógica para procesar la reserva (PENDIENTE)
    return render(request, 'reservas/reservar.html') 


# Renderiza la plantilla de confirmación de reserva exitosa
def reserva_exito_view(request):
    return render(request, 'reservas/reserva_exito.html')


