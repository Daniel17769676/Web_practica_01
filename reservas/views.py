from django.shortcuts import render, redirect
from django.http import JsonResponse
from servicios.models import Disponibilidad
from reservas.models import Servicio, Reserva #Importa los modelos de la app RESERVAS
from django.views.decorators.http import require_GET
from django.contrib import messages
from datetime import datetime, time, timedelta, date
from django.db.models import Q
from django.core.mail import EmailMessage
from ics import Calendar, Event
import arrow




# Vista para mostrar los servicios disponibles (GET)
def reservar_servicios_view(request):
    # Si es POST, redirige a la vista de procesamiento
    if request.method == 'POST':
        return procesar_reserva_view(request)
    
    # Lógica original para GET
    servicios = Disponibilidad.objects.values_list('servicio', flat=True).distinct() #Obtiene los datos de la tabla disponibilidad y unicamente 'values_list' los valores del campo 'servicio' y los devuelve como una lista de valores únicos.
    
    if request.method == 'GET' and 'servicio' in request.GET:
        servicio_seleccionado = request.GET.get('servicio') # Obtiene el servicio seleccionado del formulario
        disponibilidades = Disponibilidad.objects.filter(servicio__iexact=servicio_seleccionado) 

        return JsonResponse({'disponibilidades': list(disponibilidades.values( 'id', 'hora_inicio', 'hora_fin', 'intervalo', 'ubicacion', 'fecha_inicio', 'fecha_fin', 'disponible'))})

    return render(request, 'reservas/reservar.html', {'servicios': servicios})


        























#TRABAJAR EN  VISTAS DE PROCESAR RESERVAR Y ENVIAR ARCHIVOS .ICS POR CORREO ELECTRÓNICO
        
# Vista para procesar la reserva (POST)
def procesar_reserva_view(request):  
    try:
        # Obtener datos del formulario
        servicio_nombre = request.POST.get('servicio')        
        dia_semana = request.POST.get('dia')        
        horario = request.POST.get('horario')        
        nombre_cliente = request.POST.get('nombre')        
        telefono_cliente = request.POST.get('telefono')        
        email_cliente = request.POST.get('email')        
        observaciones = request.POST.get('observaciones', '')
        

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
        return redirect('reservas:reserva_exito', reserva_id=reserva.id) #Reserva.id es el ID de la reserva que acabamos de crear. Redirige a la vista de confirmación con el ID de la reserva recién creada.
    
    except Exception as e:        
        print(f'Error al procesar la reserva: {str(e)}') 
        return redirect('reservas:reservar')
        
    
    
# Vista para mostrar la confirmación de la reserva y enviar el archivo .ICS por correo
def reserva_exito_view(request, reserva_id):
    return render(request, 'reservas/reserva_exito.html')

