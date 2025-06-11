from django.shortcuts import render, redirect
from .models import Disponibilidad, ServicioDia
from django.contrib import messages



# Vista para CREAR disponibilidades (ADMINISTRADOR)  
def disponibilidad_view(request):
    #Para mostrar servicios disponibles (GET), EL GET es un método HTTP que se utiliza para solicitar datos de un recurso específico. En este caso, se utiliza para mostrar los servicios disponibles del administrador/oferente
    servicios_disponibles = Disponibilidad.objects.all() #Filtra las disponibilidades la base de datos.
    
    if request.method == 'POST':
        print("DATOS RECIBIDOS:", request.POST) #Imprime los datos recibidos en la consola para depuración.
        
        # 1. Primero creamos la Disponibilidad sin los días
        disponibilidad=Disponibilidad.objects.create(
            administrador=request.POST['administrador'],
            hora_inicio=request.POST['hora_inicio'],
            hora_fin=request.POST['hora_fin'],
            servicio=request.POST['servicio'],
            disponible=True # esta linea guarda el valor de la casilla de verificación y lo convierte en un booleano, un booleano es un tipo de dato que solo puede tener dos valores: verdadero o falso.
            )

        # 2. Obtenemos los días seleccionados (usamos getlist para checkboxes)
        dias_seleccionados = request.POST.getlist('dias_semana') #getlist se utiliza para obtener una lista de valores de un campo de formulario que puede tener múltiples selecciones, como casillas de verificación.
        
        # 3. Creamos un registro en ServicioDia por cada día seleccionado
        for dia in dias_seleccionados:
            ServicioDia.objects.create(
                disponibilidad=disponibilidad,
                dia=dia
            )   

        return redirect('servicios_administrador:confirmacion') #Redirect es una función que redirige al usuario a otra URL después de que se haya procesado el formulario. En este caso, redirige a la plantilla 'Confirmacion.html' después de guardar la disponibilidad en la base de datos.
    return render(request, 'mi_web/Disponibilidad.html' ,{servicios_disponibles: servicios_disponibles, #la variable 'servicios_disponibles' se pasa al contexto de la plantilla para que pueda ser utilizada en la vista.
     'dias_opciones': ServicioDia.OPCIONES_DIAS}) # 'dias_opciones' se pasa al contexto de la plantilla para que pueda ser utilizada en la vista. 'ServicioDia.OPCIONES_DIAS' es una lista de tuplas que contiene los días de la semana y sus nombres legibles para el usuario.)

# Vista para confirmar datos guardados al ofrecer disponibilidad (ADMINISTRADOR)
def confirmacion_view(request):
    return render(request, 'mi_web/Confirmacion.html')