import locale
from django.shortcuts import render, redirect
from django.http import JsonResponse
from servicios.models import Disponibilidad, Servicio
from reservas.models import Reserva #Importa los modelos de la app RESERVAS
from django.views.decorators.http import require_GET
from django.contrib import messages
from datetime import datetime, time, timedelta, date
from django.db.models import Q
from django.core.mail import EmailMessage
from ics import Calendar, Event
import arrow
from django.db import transaction
from django.db.models import OuterRef, Subquery
from django.utils import timezone




# Vista para mostrar los servicios disponibles (GET)
def obtener_servicios(request):
    # Si es POST, redirige a la vista de procesamiento
    if request.method == 'POST':
        return procesar_reserva_view(request)
    
    # Lógica original para GET
    servicios = Servicio.objects.annotate(
        admin_nombre=Subquery(
            Disponibilidad.objects.filter(servicio=OuterRef('pk'))
            .order_by('id')
            .values('administrador')[:1]
        )
    ).values_list('id', 'nombre', 'admin_nombre')


    if request.method == 'GET' and 'servicio_id' in request.GET:
        servicio_id = request.GET.get('servicio_id') # Obtiene el id seleccionado del formulario
        disponibilidades = Disponibilidad.objects.filter(servicio__id=servicio_id).values(
            'id', 'hora_inicio', 'hora_fin', 'intervalo', 
            'ubicacion', 'fecha_inicio', 'fecha_fin', 'disponible'
        )
      

        return JsonResponse({'disponibilidades': list(disponibilidades)}) # Devuelve las disponibilidades en formato JSON

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
            hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
            hora_fin = datetime.strptime(hora_fin_str, '%H:%M').time()
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
                estado='pendiente'
            )

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
        return render(request, 'reservas/error.html', {'mensaje': 'La reserva no existe'})
    except Exception as e:
        # Manejar otros errores
        return render(request, 'reservas/error.html', {'mensaje': str(e)})

