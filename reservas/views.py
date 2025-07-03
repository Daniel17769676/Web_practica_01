from django.shortcuts import render, redirect
from django.http import JsonResponse
from servicios.models import Disponibilidad, ServicioDia #Importa los modelos de la app SERVICIOS
from reservas.models import Servicio, Reserva #Importa los modelos de la app RESERVAS
from django.views.decorators.http import require_GET
from django.contrib import messages
from datetime import datetime, time, timedelta




# Vista para mostrar los servicios disponibles (GET)
def reservar_servicios_view(request):
    # Si es POST, redirige a la vista de procesamiento
    if request.method == 'POST':
        return procesar_reserva_view(request)
    
    # Lógica original para GET
    servicios = Disponibilidad.objects.values_list('servicio', flat=True).distinct()
    dias = ServicioDia.objects.values_list('dia', flat=True).distinct()

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
    try:
        # Obtener datos del formulario
        servicio_nombre = request.POST.get('servicio')
        print(f'Servicio recibido: {servicio_nombre}')  # Debugging
        dia_semana = request.POST.get('dia')
        print(f'Día recibido: {dia_semana}')  # Debugging
        horario = request.POST.get('horario')
        print(f'Horario recibido: {horario}')  # Debugging
        nombre_cliente = request.POST.get('nombre')
        print(f'Nombre del cliente recibido: {nombre_cliente}')  # Debugging
        telefono_cliente = request.POST.get('telefono')
        print(f'Teléfono del cliente recibido: {telefono_cliente}')  # Debugging
        email_cliente = request.POST.get('email')
        print(f'Email del cliente recibido: {email_cliente}')  # Debugging
        observaciones = request.POST.get('observaciones', '')
        print(f'Observaciones recibidas: {observaciones}')  # Debugging

        # Validar que todos los campos requeridos están presentes
        if not all([servicio_nombre, dia_semana, horario, nombre_cliente, telefono_cliente, email_cliente]):
            messages.error(request, 'Todos los campos son obligatorios')
            return redirect('reservas:reservar')

        # Procesar el horario (asumiendo formato "HH:MM - HH:MM")
        hora_inicio_str, hora_fin_str = horario.split(' - ')
        hora_inicio = time.fromisoformat(hora_inicio_str)
        hora_fin = time.fromisoformat(hora_fin_str)

        # Validar que el día de la semana sea válido
        DIAS_VALIDOS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        if dia_semana.lower() not in DIAS_VALIDOS:
            messages.error(request, 'Día de la semana no válido')
            return redirect('reservas:reservar')

        # Obtener o crear el servicio
        servicio, created = Servicio.objects.get_or_create(
            nombre=servicio_nombre,
            defaults={
                'descripcion': servicio_nombre,
                'duracion': timedelta(hours=1),  # Ajusta según necesites
                'activo': True
            }
        )

        # Crear la reserva
        reserva = Reserva.objects.create(
            servicio=servicio,
            dia_semana=dia_semana.lower(),
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            cliente_nombre=nombre_cliente,
            cliente_email=email_cliente,
            cliente_telefono=telefono_cliente,  # Asegúrate de agregar este campo al modelo si lo necesitas
            observaciones=observaciones,
            estado='pendiente'
        )

        # Redirigir a página de éxito
        return redirect('reservas:reserva_exito')
    
    except Exception as e:        
        print(f'Error al procesar la reserva: {str(e)}') 
        return redirect('reservas:reservar')
        
    
    
# Renderiza la plantilla de confirmación de reserva exitosa
def reserva_exito_view(request):
    return render(request, 'reservas/reserva_exito.html')


