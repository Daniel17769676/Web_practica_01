from django.shortcuts import render, redirect #importamos la función render
from django.contrib import messages

from .models import Usuario  #importamos la clase usuario de models.py  

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