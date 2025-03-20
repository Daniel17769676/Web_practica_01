from django.shortcuts import render, redirect #importamos la función render
from django.contrib import messages
from ics import Calendar, Event
from django.core.mail import EmailMessage
from .models import Reserva
from datetime import datetime, timedelta


# Creamos la vista home, que sirve para mostrar la página de inicio
def Portada(request):  
    return render(request, 'Portada.html') 

                  
def reservas_view(request):
    if request.method == 'POST':
        #Se capturan los datos de la reserva
        nombre = request.POST['nombre']
        rut = request.POST['rut']
        cargo = request.POST['cargo']
        email = request.POST['email']
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        #Se guardan los datos en la base de datos
        reserva = Reserva(nombre=nombre, rut=rut, cargo=cargo, email=email, fecha=fecha, hora=hora)
        reserva.save()

        #Enviar correo de confirmación
        enviar_correo_reserva(reserva)

        # Mostrar mensaje de éxito
        messages.success(request, 'Reserva realizada correctamente. Revisa tu correo para la confirmación.')
               
        return redirect('reserva_confirmacion', reserva_id=reserva.id)
    else:
        messages.error(request, 'Error al realizar la reserva.')           
        return render(request, 'Reservas.html')
    

def reserva_confirmacion_view(request, reserva_id):
        #obtener la reserva por su id
        reserva = Reserva.objects.get(id=reserva_id)

        #pasar los datos de la reserva al contexto
        context = {
            'nombre': reserva.nombre,
            'rut': reserva.rut,
            'cargo': reserva.cargo,
            'email': reserva.email,
            'fecha': reserva.fecha,
            'hora': reserva.hora,           
        }
        
        #renderizar la plantilla de confirmación de reserva
        return render(request, 'reserva_confirmacion.html', context)

def enviar_correo_reserva(reserva):
    # Crear el archivo .ics
    c = Calendar()
    e = Event()
    e.name = "Agendamiento de Reserva"
    e.begin = f'{reserva.fecha} {reserva.hora}'  # Combina la fecha y la hora
    e.duration = timedelta(minutes=15)
    e.description = f"Reserva para {reserva.nombre}."
    c.events.add(e)
    
     # Crear el archivo .ics
    ics_filename = f"{reserva.nombre}_reserva.ics"
    with open(ics_filename, 'w') as f:
        f.writelines(c)

    # Crear el correo electrónico
    email = EmailMessage(
        'Confirmación de Reserva',
        f'Hola {reserva.nombre}, tu reserva ha sido confirmada para el {reserva.fecha} a las {reserva.hora}.',
        'from@example.com',  # Cambiar por el correo del remitente real
        [reserva.email],      # Se envía al correo del cliente
    )
    
    # Adjuntar el archivo .ics
    email.attach_file(ics_filename)
    
    # Enviar el correo
    email.send()

def reservas(request):
    # Simulación de horas disponibles (puedes obtenerlas de la base de datos)
    horas_disponibles = [
        "09:00 AM",
        "21:00 PM"
        ]

    # Puedes filtrar horas ya reservadas desde tu modelo
    fecha_seleccionada = request.GET.get("fecha")

    if fecha_seleccionada:
        # Consultar las horas ocupadas en la base de datos para esa fecha
        horas_ocupadas = Reserva.objects.filter(fecha=fecha_seleccionada).values_list('hora', flat=True)
        
      # Filtrar las horas disponibles eliminando las ocupadas
        horas_disponibles = [hora for hora in horas_disponibles if hora not in horas_ocupadas]

    return render(request, "mi_web/reservas.html", {"horas_disponibles": horas_disponibles})