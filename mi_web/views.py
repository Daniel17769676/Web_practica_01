from django.shortcuts import render, redirect #importamos la función render
from django.contrib import messages
from ics import Calendar, Event
from django.core.mail import EmailMessage
import datetime
from .models import Usuario, Reserva


# Creamos la vista home, que sirve para mostrar la página de inicio
def Portada(request):  
    return render(request, 'Portada.html') 

def Registro(request):  
    return render(request, 'Registro.html')

def Login(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        password = request.POST['password']

        # Verificar si el usuario existe
        try:
            usuario = Usuario.objects.get(user=usuario, password=password)
            messages.success(request, f'Bienvenido {usuario.nombre}')
            return redirect('reservas')
        
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    #Si el usuario no existe, se redirige al login
    return render(request, 'Login.html')
              
def nuevo_usuario(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        nombre = request.POST['nombre']
        email = request.POST['email']
        password = request.POST['password']


        # Imprime los datos capturados para depuración
        print(f"Creando usuario: {usuario}, {email}")  # Esto muestra los valores capturados

        # Verificar si el nombre de usuario ya existe
        if Usuario.objects.filter(user=usuario).exists():
            messages.error(request, 'El usuario ya existe.')
            return render(request, 'Registro.html')

        # Crear el usuario
        nuevo_usuario = Usuario(user=usuario, nombre=nombre, email=email, password=password)
        nuevo_usuario.save() # Guardar el usuario en la base de datos
     
        messages.success(request, 'Usuario registrado correctamente, redirigiendo al LOGIN')
        return redirect('login')
    else:
        return render(request, 'Registro.html')
    
def reserva_view(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        rut = request.POST['rut']
        cargo = request.POST['cargo']
        email = request.POST['email']
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        
        reserva = Reserva(nombre=nombre, rut=rut, cargo=cargo, email=email, fecha=fecha, hora=hora)
        reserva.save()

        messages.success(request, 'Reserva realizada correctamente.')
        return redirect('reserva_confirmacion')
    else:
        messages.error(request, 'Error al realizar la reserva.')           
        return render(request, 'reserva_form.html')

def reserva_confirmacion_view(request):
    return render(request, 'reserva_confirmacion.html')

def enviar_correo_reserva(reserva):
    c = Calendar()
    e = Event()
    e.name = "Sesión de Masajes"
    e.begin = reserva.hora
    e.duration = datetime.timedelta(minutes=15)
    e.description = f"Reserva de masaje para {reserva.nombre}."
    c.events.add(e)
    
    with open(f"{reserva.nombre}.ics", 'w') as f:
        f.writelines(c)
    
    email = EmailMessage(
        'Confirmación de Reserva de Masajes',
        f'Hola {reserva.nombre}, tu reserva ha sido confirmada para el {reserva.fecha}.',
        'from@example.com',
        [reserva.email],
    )
    email.attach_file(f"{reserva.nombre}.ics")
    email.send()