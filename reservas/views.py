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


# Vista para obtener los días disponibles por servicio (GET)
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
    
#vista para obtener los horarios disponibles por servicio y día (GET)
def get_horarios(request):
    servicio = request.GET.get('servicio', '').strip().lower()
    dia = request.GET.get('dia', '').strip().lower()
    
    if not servicio or not dia:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)
    
    try:
        # 1. Obtener disponibilidades activas
        disponibilidades = Disponibilidad.objects.filter(
            servicio__iexact=servicio,
            dias__dia__iexact=dia,
            disponible=True
        ).prefetch_related('dias')

        # 2. Obtener horarios reservados (aunque sabemos que está vacío)
        reservados = Reserva.objects.filter(
            servicio__nombre__iexact=servicio,
            dia_semana__iexact=dia,
            estado__in=['confirmada', 'pendiente']
        ).values_list('hora_inicio', 'hora_fin')

        # 3. Convertir horarios reservados a formato comparable
        reservados_set = {
            (hora_inicio.strftime('%H:%M'), hora_fin.strftime('%H:%M'))
            for hora_inicio, hora_fin in reservados
        }

        # 4. Generar horarios disponibles
        horarios_disponibles = []
        for disp in disponibilidades:
            for turno in disp.get_turnos():
                inicio = turno['inicio'].strftime('%H:%M')
                fin = turno['fin'].strftime('%H:%M')
                
                if (inicio, fin) not in reservados_set:
                    horarios_disponibles.append(f"{inicio} - {fin}")

        return JsonResponse({
            'horarios': horarios_disponibles,
            'total_disponibles': len(horarios_disponibles),
            'status': 'success'
        })
    
    except Exception as e:
        return JsonResponse({
            'error': f"Error al procesar horarios: {str(e)}",
            'status': 'error'
        }, status=500)
    

        
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
    reserva = Reserva.objects.get(id=reserva_id)
    
    # Asumimos que la reserva es para hoy (ajusta según tu lógica)
    fecha_actual = date.today()
    
    # Crear el archivo .ICS
    cal = Calendar()
    
    # Combinar fecha actual con las horas de reserva
    inicio_datetime = datetime.combine(fecha_actual, reserva.hora_inicio)
    fin_datetime = datetime.combine(fecha_actual, reserva.hora_fin)
    
    # Convertir a objeto arrow con zona horaria
    inicio = arrow.get(inicio_datetime).to('local')
    fin = arrow.get(fin_datetime).to('local')
    
    event = Event(
        name=f"Reserva: {reserva.servicio.nombre}",
        begin=inicio.datetime,
        end=fin.datetime,
        description=f"""
        Detalles de la reserva:
        Servicio: {reserva.servicio.nombre}
        Cliente: {reserva.cliente_nombre}
        Teléfono: {reserva.cliente_telefono}
        Email: {reserva.cliente_email}
        Día: {reserva.dia_semana}
        Hora: {reserva.hora_inicio.strftime('%H:%M')} - {reserva.hora_fin.strftime('%H:%M')}
        """,
        location="Ubicación del servicio",  # Ajusta esto
        attendees=[reserva.cliente_email]
    )
    
    cal.events.add(event)
    
    # Enviar por correo
    email = EmailMessage(
        subject=f"Confirmación de reserva - {reserva.servicio.nombre}",
        body=f"""
        Hola {reserva.cliente_nombre},
        
        Tu reserva ha sido confirmada:
        
        Servicio: {reserva.servicio.nombre}
        Día: {reserva.dia_semana}
        Hora: {reserva.hora_inicio.strftime('%H:%M')} - {reserva.hora_fin.strftime('%H:%M')}
        
        Se ha adjuntado un recordatorio para tu calendario.
        """,
        from_email="tusistema@tudominio.com",
        to=[reserva.cliente_email],
    )
    
    # Adjuntar el .ICS
    email.attach('reserva.ics', cal.serialize(), 'text/calendar')
    
    try:
        email.send()
        print("Correo con ICS enviado exitosamente")
    except Exception as e:
        print(f"Error enviando correo: {e}")
    
    return render(request, 'reservas/reserva_exito.html', {
        'servicio': reserva.servicio,
        'cliente_nombre': reserva.cliente_nombre,
        'dia_semana': reserva.dia_semana,
        'hora_inicio': reserva.hora_inicio,
        'hora_fin': reserva.hora_fin,
        'cliente_telefono': reserva.cliente_telefono,
        'cliente_email': reserva.cliente_email,
    })