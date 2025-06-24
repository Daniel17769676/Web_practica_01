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

    # Si la petición es GET y se ha seleccionado un servicio, obtenemos las disponibilidades y los días disponibles y retornamos un JSON
    if request.method == 'GET' and 'servicio' in request.GET:
        servicio_seleccionado = request.GET.get('servicio')
        disponibilidades = Disponibilidad.objects.filter(servicio=servicio_seleccionado)
        
        dias_disponibles = ServicioDia.objects.filter(
            disponibilidad__in=disponibilidades
        ).values_list('dia', flat=True).distinct()
        
        return JsonResponse({
            'dias': list(dias_disponibles),
            'disponibilidades': list(disponibilidades.values(
                'id', 'hora_inicio', 'hora_fin', 'intervalo'
            ))
        })    

    return render(request, 'reservas/reservar.html', {'servicios': servicios, 'dias': dias, 'horarios': []})

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
    

def get_horarios(request):
    servicio = request.GET.get('servicio', '').strip().lower()
    dia = request.GET.get('dia', '').strip().lower()
    
    if not servicio or not dia:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)
    
    try:
        disponibilidades = Disponibilidad.objects.filter(
            servicio__iexact=servicio,
            dias__dia__iexact=dia
        ).prefetch_related('dias')
        
        horarios = []
        for disp in disponibilidades:
            for turno in disp.get_turnos():
                horarios.append(
                    f"{turno['inicio']} - {turno['fin']}"
                )
        
        return JsonResponse({'horarios': horarios})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

        
# Vista para procesar la reserva (POST)
def procesar_reserva_view(request):
    #Agregar la lógica para procesar la reserva (PENDIENTE)
    return render(request, 'reservas/reservar.html') 


# Renderiza la plantilla de confirmación de reserva exitosa
def reserva_exito_view(request):
    return render(request, 'reservas/reserva_exito.html')


