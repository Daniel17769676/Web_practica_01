from django.shortcuts import render, redirect
from .models import Disponibilidad, ServicioDia
from datetime import time, timedelta, datetime



# Vista para CREAR disponibilidades (ADMINISTRADOR)  
def disponibilidad_view(request):
    #Para mostrar servicios disponibles (GET), EL GET es un método HTTP que se utiliza para solicitar datos de un recurso específico. En este caso, se utiliza para mostrar los servicios disponibles del administrador/oferente
    servicios_disponibles = Disponibilidad.objects.all() #Filtra las disponibilidades la base de datos.
    
    if request.method == 'POST':      
                
            # 1. Primero creamos la Disponibilidad con todos los campos
            disponibilidad=Disponibilidad.objects.create(
                administrador=request.POST['administrador'],
                hora_inicio=request.POST['hora_inicio'],
                hora_fin=request.POST['hora_fin'],
                servicio=request.POST['servicio'],
                disponible=True, # esta linea guarda el valor de la casilla de verificación y lo convierte en un booleano, un booleano es un tipo de dato que solo puede tener dos valores: verdadero o falso.
                intervalo = int(request.POST.get('intervalo'))) #Obtenemos el intervalo de tiempo en minutos entre cada disponibilidad.
        
            # 2. Procesar días seleccionados
            dias_seleccionados = request.POST.getlist('dias_semana') #getlist se utiliza para obtener una lista de valores de un campo de formulario que puede tener múltiples selecciones, como casillas de verificación.
            

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

        
            # 4. Creamos un registro en ServicioDia por cada día seleccionado
            for dia in dias_seleccionados:
                ServicioDia.objects.create(
                    disponibilidad=disponibilidad,
                    dia=dia
                )   

            

            return redirect('servicios:confirmacion', disponibilidad_id=disponibilidad.id) #disponibilidad.id es el ID de la disponibilidad que acabamos de crear. Redirige a la vista de confirmación con el ID de la disponibilidad recién creada.
   
    return render(request, 'mi_web/Disponibilidad.html' ,{servicios_disponibles: servicios_disponibles, #la variable 'servicios_disponibles' se pasa al contexto de la plantilla para que pueda ser utilizada en la vista.
     'dias_opciones': ServicioDia.OPCIONES_DIAS}) # 'dias_opciones' se pasa al contexto de la plantilla para que pueda ser utilizada en la vista. 'ServicioDia.OPCIONES_DIAS' es una lista de tuplas que contiene los días de la semana y sus nombres legibles para el usuario.)

# Vista para confirmar datos guardados al ofrecer disponibilidad (ADMINISTRADOR)
def confirmacion_view(request, disponibilidad_id):
    disponibilidad = Disponibilidad.objects.get(id=disponibilidad_id) # Obtiene la disponibilidad por su ID
    print("Datos de disponibilidad:", disponibilidad.__dict__)  # Debug
    dias = ServicioDia.objects.filter(disponibilidad=disponibilidad) # Obtiene los días asociados a la disponibilidad
    return render(request, 'mi_web/Confirmacion.html', {
        'administrador': disponibilidad.administrador,
        'servicio': disponibilidad.servicio,
        'dias': [dia.get_dia_display() for dia in dias],  # Muestra el nombre del día (ej: "Lunes")
        'horario': f"{disponibilidad.hora_inicio} - {disponibilidad.hora_fin}",
        'estado': "Confirmado" if disponibilidad.disponible else "Pendiente",
    })
    