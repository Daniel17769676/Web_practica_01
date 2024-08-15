from django.shortcuts import render, redirect #importamos la función render
from django.contrib import messages
from .forms import ReservaForm
from .models import Reserva
from ics import Calendar, Event
from django.core.mail import EmailMessage
import datetime


from .models import Usuario  #importamos la clase usuario de models.py  
from .models import Reserva 

# Creamos la vista home, que sirve para mostrar la página de inicio
def Portada(request):  
    return render(request, 'Portada.html') 

def Registro(request):  
    return render(request, 'Registro.html')

def Login(request):
    return render(request, 'Login.html')

def nuevo_usuario(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        nombre = request.POST['nombre']
        email = request.POST['email']
        password = request.POST['password']
        nuevo_usuario = Usuario(usuario=usuario, nombre=nombre, email=email, password=password)
        nuevo_usuario.save()

        messages.success(request, 'Usuario registrado correctamente, redirigiendo al LOGIN')
        return redirect('login')
    else:
        messages.error(request, 'Error al registrar el usuario')
        return render(request, 'Registro.html')
    
def reserva_view(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save()
            enviar_correo_reserva(reserva)  # Función para enviar el correo
            return redirect('reservas')
    else:
        form = ReservaForm()
    return render(request, 'reserva_form.html', {'form': form})

def reserva_confirmacion_view(request):
    return render(request, 'reserva_confirmacion.html')

def enviar_correo_reserva(reserva):
    c = Calendar()
    e = Event()
    e.name = "Sesión de Masajes"
    e.begin = reserva.horario
    e.duration = datetime.timedelta(minutes=15)
    e.description = f"Reserva de masaje para {reserva.nombre}."
    c.events.add(e)
    
    with open(f"{reserva.nombre}.ics", 'w') as f:
        f.writelines(c)
    
    email = EmailMessage(
        'Confirmación de Reserva de Masajes',
        f'Hola {reserva.nombre}, tu reserva ha sido confirmada para el {reserva.horario}.',
        'from@example.com',
        [reserva.email],
    )
    email.attach_file(f"{reserva.nombre}.ics")
    email.send()