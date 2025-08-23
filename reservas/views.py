import locale
from django.shortcuts import render, redirect
from django.http import JsonResponse
from servicios.models import Disponibilidad, Servicio
from reservas.models import Reserva
from django.contrib import messages
from datetime import datetime, timedelta, date
from django.core.mail import EmailMessage
from ics import Calendar, Event
from django.db.models import OuterRef, Subquery
from django.conf import settings
import pytz
from ics.alarm import DisplayAlarm
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt




# Vista para obtener horarios reservados desde la BBDD
@csrf_exempt
def obtener_horarios_reservados(request):
    if request.method == 'GET':
        servicio_id = request.GET.get('servicio_id')
        fecha = request.GET.get('fecha')
        
        if servicio_id and fecha:
            try:
                horarios_reservados = Reserva.objects.filter(
                    disponibilidad__servicio_id=servicio_id,
                    fecha_reserva=fecha
                ).values_list('horario', flat=True)
                
                # Normalizar los horarios para consistencia
                horarios_normalizados = []
                for horario in horarios_reservados:
                    if horario:
                        # Asegurar formato consistente: "HH:MM - HH:MM"
                        partes = horario.split('-')
                        if len(partes) == 2:
                            inicio = partes[0].strip()
                            fin = partes[1].strip()
                            
                            # Normalizar formato de tiempo
                            for i, tiempo in enumerate([inicio, fin]):
                                if ':' in tiempo:
                                    h, m = tiempo.split(':')
                                    h = h.strip().zfill(2)  # Asegurar 2 dígitos
                                    m = m.strip().zfill(2)  # Asegurar 2 dígitos
                                    if i == 0:
                                        inicio = f"{h}:{m}"
                                    else:
                                        fin = f"{h}:{m}"
                            
                            horario_normalizado = f"{inicio} - {fin}"
                            horarios_normalizados.append(horario_normalizado)
                
                return JsonResponse({
                    'status': 'success',
                    'horarios_reservados': horarios_normalizados
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Parámetros inválidos'
    }, status=400)



# Vista para mostrar los servicios disponibles (GET)
def obtener_servicios(request):
    if 'servicio_id' in request.GET:
        servicio_id = request.GET.get('servicio_id')
        
        # Obtener horarios reservados si se proporciona fecha
        horarios_reservados = []
        if 'fecha' in request.GET:
            fecha = request.GET.get('fecha')
            horarios_reservados = Reserva.objects.filter(
                disponibilidad__servicio_id=servicio_id,
                fecha_reserva=fecha
            ).values_list('horario', flat=True)
        
        disponibilidades = Disponibilidad.objects.filter(servicio__id=servicio_id).values(
            'id', 'hora_inicio', 'hora_fin', 'intervalo', 
            'ubicacion', 'fecha_inicio', 'fecha_fin', 'disponible'
        )
        
        return JsonResponse({
            'disponibilidades': list(disponibilidades),
            'horarios_reservados': list(horarios_reservados)
        })
    
    # Si no es una solicitud con servicio_id, renderizar la página normal
    servicios = Servicio.objects.annotate(
        admin_nombre=Subquery(
            Disponibilidad.objects.filter(servicio=OuterRef('pk'))
            .order_by('id')
            .values('administrador')[:1]
        )
    ).values_list('id', 'nombre', 'admin_nombre')
    
    return render(request, 'reservas/reservar.html', {'servicios': servicios})

     
def procesar_reserva_view(request):  
    if request.method == 'POST':
        # 1. Obtener los datos del formulario
        disponibilidad_id = request.POST.get('disponibilidad_id')
        servicio_id = request.POST.get('servicio') 
        fecha_reserva = request.POST.get('fecha_reserva')
        horario = request.POST.get('horario')  # Este debería ser el horario específico "HH:MM - HH:MM"
        
        # Extraer hora_inicio y hora_fin del horario
        try:
            hora_inicio_str, hora_fin_str = horario.split(' - ')
            # Asegurar formato HH:MM
            hora_inicio = datetime.strptime(hora_inicio_str.strip(), '%H:%M').time()
            hora_fin = datetime.strptime(hora_fin_str.strip(), '%H:%M').time()
            
            # Reconstruir horario en formato consistente
            horario = f"{hora_inicio.strftime('%H:%M')} - {hora_fin.strftime('%H:%M')}"
            
        except:
            messages.error(request, 'Formato de horario inválido')
            return redirect('reservas:obtener_servicios')

        try:
            # 2. Convertir fecha
            fecha_reserva = datetime.strptime(fecha_reserva, '%Y-%m-%d').date()
            
            # 3. Verificar reserva existente para este horario específico
            if Reserva.objects.filter(
                disponibilidad_id=disponibilidad_id,
                fecha_reserva=fecha_reserva,
                horario=horario  # Ahora verificamos el horario exacto
            ).exists():
                messages.error(request, 'Este horario ya ha sido reservado')
                return redirect('reservas:obtener_servicios')
            
            
            

            
            
            # 4. Crear la reserva (sin marcar toda la disponibilidad como False)
            reserva = Reserva.objects.create(
                disponibilidad_id=disponibilidad_id,
                fecha_reserva=fecha_reserva,
                horario=horario,
                cliente_nombre=request.POST.get('nombre'),
                cliente_rut=request.POST.get('rut'),
                cliente_email=request.POST.get('email'),
                cliente_telefono=request.POST.get('telefono'),
                observaciones=request.POST.get('observaciones', ''),
                estado='confirmada'  # Estado inicial de la reserva     
            )

            # --- Generar archivo .ics ---
            timezone = pytz.timezone('America/Santiago')  # Ajusta según tu zona horaria
            
            # Convertir fecha y hora a datetime con zona horaria
            inicio = timezone.localize(
                datetime.combine(reserva.fecha_reserva, hora_inicio)  # Usa hora_inicio (datetime.time)
            )
            fin = timezone.localize(
                datetime.combine(reserva.fecha_reserva, hora_fin)  # Usa hora_fin (datetime.time)
            )

            # Opcional: Calcula duración automáticamente
            duracion = datetime.combine(date.min, hora_fin) - datetime.combine(date.min, hora_inicio)
          
            # Crear evento ICS
            calendar = Calendar()
            event = Event()
            event.name = f"Reserva: {reserva.disponibilidad.servicio.nombre}"
            event.begin = inicio
            event.end = fin
            event.duration = duracion  # Usa la duración calculada
            event.description = (
                f"Cliente: {reserva.cliente_nombre}\n"
                f"Teléfono: {reserva.cliente_telefono}\n"
                f"Email: {reserva.cliente_email}\n"
                f"Observaciones: {reserva.observaciones or 'Ninguna'}"
            )
            event.location = reserva.disponibilidad.ubicacion or "Ubicación no especificada"
            calendar.events.append(event)

            # --- Añadir alarma/alertas al .ICS---
            alarma = DisplayAlarm()
            alarma.trigger = timedelta(minutes=-5)  # 5 minutos antes
            alarma.display_text = f"Recordatorio: Reserva de {reserva.disponibilidad.servicio.nombre}"
            
            event.alarms.append(alarma)  # Añadir alarma al evento

            # Guardar archivo temporal
            ics_content = str(calendar)
            
            # --- Enviar por email ---
            email = EmailMessage(
                subject=f"Confirmación de reserva - {reserva.disponibilidad.servicio.nombre}",
                body=f"""
                Hola {reserva.cliente_nombre},
                
                Tu reserva para {reserva.disponibilidad.servicio.nombre} ha sido confirmada.
                
                Detalles:
                - Fecha: {reserva.fecha_reserva.strftime('%d/%m/%Y')}
                - Hora: {reserva.horario}
                - Ubicación: {reserva.disponibilidad.ubicacion or 'Por confirmar'}
                
                Adjunto encontrarás el evento para tu calendario.
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[reserva.cliente_email],
                cc=[],  # Puedes añadir CC si es necesario
            )
            
            email.attach(
                filename=f"reserva_{reserva.id}.ics",
                content=ics_content,
                mimetype="text/calendar"
            )
            email.send()            

            return redirect('reservas:reserva_exito', reserva_id=reserva.id)

        except Exception as e:
            print(f'Error al procesar reserva: {str(e)}')
            messages.error(request, f'Ocurrió un error al procesar la reserva: {str(e)}')
            return redirect('reservas:obtener_servicios')
    
    
# Vista para mostrar la confirmación de la reserva y enviar el archivo .ICS por correo
def reserva_exito_view(request, reserva_id):
    # Configurar locale para español (con manejo de errores)
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES')
        except locale.Error:
            locale.setlocale(locale.LC_TIME, 'spanish')

    try:
        reserva = Reserva.objects.get(id=reserva_id)
        servicio = Servicio.objects.get(id=reserva.disponibilidad.servicio.id)
        
        # Función mejorada para formatear fechas
        def format_date(date_obj):
            if isinstance(date_obj, str):
                date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
            elif isinstance(date_obj, datetime):
                date_obj = date_obj.date()
            return date_obj.strftime('%A, %d de %B de %Y').capitalize()

        # Obtener fecha formateada
        fecha_reserva_formateada = format_date(reserva.fecha_reserva)


        context = {
            'cliente_nombre': reserva.cliente_nombre,
            'servicio': servicio,
            'fecha_reserva': fecha_reserva_formateada,  # Usar la versión formateada
            'fecha_reserva_original': reserva.fecha_reserva,  # Mantener formato original por si acaso
            'horario': reserva.horario,
            'horario_original': reserva.horario,
            'telefono': reserva.cliente_telefono,
            'cliente_email': reserva.cliente_email,
            'observaciones': reserva.observaciones,
            'reserva_id': reserva.id,
        }
        
        return render(request, 'reservas/reserva_exito.html', context)

    except Reserva.DoesNotExist:
        # Manejar error si la reserva no existe
        return render(request, 'reservas/reservar.html', {'mensaje': 'La reserva no existe'})
    except Exception as e:
        # Manejar otros errores
        return render(request, 'reservas/reservar.html', {'mensaje': str(e)})

def panel_reservas_view(request):
    # Consulta optimizada que incluye todas las relaciones necesarias
    reservas = Reserva.objects.select_related(
        'disponibilidad__servicio'  # Carga el servicio a través de disponibilidad
    ).order_by('-fecha_reserva', '-horario')
    
    if not reservas.exists():
        messages.info(request, 'No hay reservas registradas.')
    
    return render(request, 'reservas/panel_reservas.html', {'reservas': reservas})