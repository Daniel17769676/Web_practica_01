from django.shortcuts import render, redirect
from .models import Disponibilidad, Servicio
from datetime import time, timedelta, datetime



# Vista para CREAR disponibilidades (ADMINISTRADOR)  
def disponibilidad_view(request):
    #Para mostrar servicios disponibles (GET), EL GET es un método HTTP que se utiliza para solicitar datos de un recurso específico. En este caso, se utiliza para mostrar los servicios disponibles del administrador/oferente
    servicios_disponibles = Disponibilidad.objects.all() #Filtra las disponibilidades la base de datos.
    print("Método HTTP:", request.method) #Debug
    if request.method == 'POST':
            print("Datos POST:", request.POST) #Debug
            try:
                # 1. Crear el Servicio (si no existe)
                servicio, created = Servicio.objects.get_or_create(
                     nombre=request.POST['servicio'],
                     defaults={
                         'descripcion': request.POST.get('descripcion', ''),
                         'duracion': timedelta(minutes=15)
                     }
                )

                # 2. Creamos la Disponibilidad con todos los campos
                disponibilidad=Disponibilidad.objects.create(
                    administrador=request.POST['administrador'],
                    fecha_inicio=request.POST['fecha_inicio'],
                    fecha_fin=request.POST['fecha_fin'],
                    ubicacion=request.POST['ubicacion'],
                    hora_inicio=request.POST['hora_inicio'],
                    hora_fin=request.POST['hora_fin'],
                    servicio=servicio,
                    disponible=True, # esta linea guarda el valor de la casilla de verificación y lo convierte en un booleano, un booleano es un tipo de dato que solo puede tener dos valores: verdadero o falso.
                    intervalo = int(request.POST.get('intervalo', 15))) #Obtenemos el intervalo de tiempo en minutos entre cada disponibilidad.


                print("¡Registro creado! ID:", disponibilidad.id)  # Debug

                # 3.  Convertir horas y generar turnos
                hora_inicio = datetime.strptime(request.POST['hora_inicio'], '%H:%M').time()
                hora_fin = datetime.strptime(request.POST['hora_fin'], '%H:%M').time()
            
                # Crear objetos datetime para facilitar los cálculos
                inicio = datetime.combine(datetime.today(), hora_inicio)
                fin = datetime.combine(datetime.today(), hora_fin)
                intervalo = disponibilidad.intervalo  # Intervalo en minutos
            
                # Generar los turnos
                current = inicio
                while current + timedelta(minutes=intervalo) <= fin:
                    hora_inicio = current.time()
                    hora_fin = (current + timedelta(minutes=intervalo)).time()
                    current += timedelta(minutes=intervalo)       
          
      
                return redirect('servicios:confirmacion', disponibilidad_id=disponibilidad.id) #disponibilidad.id es el ID de la disponibilidad que acabamos de crear. Redirige a la vista de confirmación con el ID de la disponibilidad recién creada.
    
            except KeyError as e:
                return render(request, 'mi_web/Disponibilidad.html', {
                    'servicios_disponibles': servicios_disponibles,
                    'error': f'Falta el campo requerido: {e}'
                })
            except Exception as e:
                return render(request, 'mi_web/Disponibilidad.html', {
                    'servicios_disponibles': servicios_disponibles,
                    'error': f'Error inesperado: {str(e)}'
                })

    return render(request, 'mi_web/Disponibilidad.html', {
                    'servicios_disponibles': servicios_disponibles,
                    'servicios': Servicio.objects.all()  # Añadir esto para el select en el template
                })            




# Vista para confirmar datos guardados al ofrecer disponibilidad (ADMINISTRADOR)
def confirmacion_view(request, disponibilidad_id):
    disponibilidad = Disponibilidad.objects.get(id=disponibilidad_id) # Obtiene la disponibilidad por su ID
    print("Datos de disponibilidad:", disponibilidad.__dict__)  # Debug
    
    return render(request, 'mi_web/Confirmacion.html', {
        'administrador': disponibilidad.administrador,
        'servicio': disponibilidad.servicio,
        'fecha_inicio': disponibilidad.fecha_inicio,
        'fecha_fin': disponibilidad.fecha_fin,        
        'horario': f"{disponibilidad.hora_inicio} - {disponibilidad.hora_fin}",
        'estado': "Confirmado" if disponibilidad.disponible else "Pendiente",
    })
    