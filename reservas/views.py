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




# Vista para mostrar los servicios disponibles (GET)
def obtener_servicios(request):
    # Si es POST, redirige a la vista de procesamiento
    if request.method == 'POST':
        return procesar_reserva_view(request)
    
    # Lógica original para GET
    servicios = Servicio.objects.values_list('nombre', flat=True).distinct() #Obtiene los datos de la tabla disponibilidad y unicamente 'values_list' los valores del campo 'servicio' y los devuelve como una lista de valores únicos.
    
    if request.method == 'GET' and 'servicio' in request.GET:
        servicio_seleccionado = request.GET.get('servicio') # Obtiene el servicio seleccionado del formulario
        disponibilidades = Disponibilidad.objects.filter(servicio__nombre__iexact=servicio_seleccionado).values(
            'id', 'hora_inicio', 'hora_fin', 'intervalo', 
            'ubicacion', 'fecha_inicio', 'fecha_fin', 'disponible'
        ) 

        return JsonResponse({'disponibilidades': list(disponibilidades)})

    return render(request, 'reservas/reservar.html', {'servicios': servicios})


     
# Vista para procesar la reserva (POST)
def procesar_reserva_view(request):  
    if request.method == 'POST':
        print("Datos recibidos:", request.POST)  # Debug
        #1. Obtener los datos del formulario
        disponibilidad_id = request.POST.get('disponibilidad_id')
        servicio_nombre = request.POST.get('servicio')
        fecha_reserva = request.POST.get('fecha_reserva')
        horario = request.POST.get('horario')        
        cliente_nombre = request.POST.get('nombre')
        cliente_rut = request.POST.get('rut')
        cliente_telefono = request.POST.get('telefono')
        cliente_email = request.POST.get('email')
        observaciones = request.POST.get('observaciones', '')
        

        # Validar que todos los campos requeridos están presentes
        if not all([disponibilidad_id, servicio_nombre, fecha_reserva, horario, cliente_nombre, cliente_rut, cliente_telefono, cliente_email]):
            messages.error(request, 'Todos los campos son obligatorios')
            return redirect('reservas:obtener_servicios')
        
        try: # Convertir la fecha de reserva a un objeto date
            fecha_reserva = datetime.strptime(fecha_reserva, '%Y-%m-%d').date()  # Convertir a objeto date

            # Procesar el horario (formato "HH:MM - HH:MM")
            #hora_inicio_str, hora_fin_str = horario.split(' - ')
            #hora_inicio = time.fromisoformat(hora_inicio_str)
            #hora_fin = time.fromisoformat(hora_fin_str)

        
            # Obtener o crear el servicio
            #servicio, created = Servicio.objects.get_or_create(
            #    nombre=servicio_nombre,
            #    defaults={'descripcion': servicio_nombre,'duracion': timedelta(hours=1),'activo': True}
            #)



            # Verificar si ya existe una reserva para este servicio, fecha y horario
            reserva_existente = Reserva.objects.filter(
                servicio_nombre=servicio_nombre,
                fecha_reserva=fecha_reserva,
                horario=horario
            ).exists()

            if reserva_existente:
                messages.error(request, 'Ya existe una reserva para este servicio en la fecha y horario seleccionados')
                return redirect('reservas:obtener_servicios')

            # Crear la reserva
            reserva = Reserva.objects.create(
                disponibilidad_id=disponibilidad_id,
                servicio_nombre=servicio_nombre,
                fecha_reserva=fecha_reserva,
                horario=horario,
                cliente_nombre=cliente_nombre,
                cliente_rut=cliente_rut,
                cliente_email=cliente_email,
                cliente_telefono=cliente_telefono,
                observaciones=observaciones,
                estado='pendiente'
            )

            # Redirigir a página de éxito
            return redirect('reservas:reserva_exito', reserva_id=reserva.id) #Reserva.id es el ID de la reserva que acabamos de crear. Redirige a la vista de confirmación con el ID de la reserva recién creada.
    
        except Exception as e:        
            print(f'Error al procesar la reserva: {str(e)}')
            messages.error(request, f'Ocurrió un error al procesar la reserva {str(e)}')  
            return redirect('reservas:obtener_servicios')  # Redirige a la vista de servicios si hay un error
        
    
    
# Vista para mostrar la confirmación de la reserva y enviar el archivo .ICS por correo
def reserva_exito_view(request, reserva_id):
    return render(request, 'reservas/reserva_exito.html')

