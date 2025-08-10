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




# Vista para mostrar los servicios disponibles (GET)
def obtener_servicios(request):
    # Si es POST, redirige a la vista de procesamiento
    if request.method == 'POST':
        return procesar_reserva_view(request)
    
    # Lógica original para GET
    servicios = Servicio.objects.values_list('id', 'nombre').distinct() #Obtiene los datos de la tabla disponibilidad y unicamente 'values_list' los valores del campo 'servicio' y los devuelve como una lista de valores únicos.
    
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
        # Debug: Imprimir los datos recibidos
        print("Datos recibidos:", request.POST)

        # 1. Obtener los datos del formulario
        disponibilidad_id = request.POST.get('disponibilidad_id')
        servicio_id = request.POST.get('servicio')  # Cambiado de servicio_nombre a servicio_id
        fecha_reserva = request.POST.get('fecha_reserva')
        horario = request.POST.get('horario')        
        cliente_nombre = request.POST.get('nombre')
        cliente_rut = request.POST.get('rut')
        cliente_telefono = request.POST.get('telefono')
        cliente_email = request.POST.get('email')
        observaciones = request.POST.get('observaciones', '')

        # 2. Validación de campos requeridos
        required_fields = [
            disponibilidad_id, servicio_id, fecha_reserva, horario,
            cliente_nombre, cliente_rut, cliente_email
        ]
        if not all(required_fields):
            messages.error(request, 'Todos los campos son obligatorios')
            return redirect('reservas:obtener_servicios')
        
        try:
            # 3. Convertir y validar fecha
            fecha_reserva = datetime.strptime(fecha_reserva, '%Y-%m-%d').date()
            
            # 4. Obtener y bloquear la disponibilidad
            with transaction.atomic():
                disponibilidad = Disponibilidad.objects.select_for_update().get(
                    id=disponibilidad_id,
                    disponible=True
                )
                
                # 5. Verificar reserva existente
                if Reserva.objects.filter(
                    disponibilidad=disponibilidad,
                    fecha_reserva=fecha_reserva
                ).exists():
                    messages.error(request, 'Ya existe una reserva para este horario')
                    return redirect('reservas:obtener_servicios')
                
                # 6. Crear la reserva
                reserva = Reserva.objects.create(
                    disponibilidad=disponibilidad,
                    fecha_reserva=fecha_reserva,
                    horario=horario,
                    cliente_nombre=cliente_nombre,
                    cliente_rut=cliente_rut,
                    cliente_email=cliente_email,
                    cliente_telefono=cliente_telefono,
                    observaciones=observaciones,
                    estado='pendiente'
                )
                
                # 7. Marcar como no disponible
                disponibilidad.disponible = False
                disponibilidad.save()

                # 8. Redirigir a página de éxito
                return redirect('reservas:reserva_exito', reserva_id=reserva.id)

        except Disponibilidad.DoesNotExist:
            messages.error(request, 'El horario seleccionado ya no está disponible')
        except Exception as e:
            print(f'Error al procesar reserva: {str(e)}')
            messages.error(request, f'Ocurrió un error al procesar la reserva: {str(e)}')
        
        return redirect('reservas:obtener_servicios')
    
    
# Vista para mostrar la confirmación de la reserva y enviar el archivo .ICS por correo
def reserva_exito_view(request, reserva_id):
    return render(request, 'reservas/reserva_exito.html', {'reserva_id': reserva_id})

