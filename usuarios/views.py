from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from servicios.models import Administrador
from django.contrib.auth.decorators import login_required


@login_required
def panel_administrador(request):
    # Verifica que el usuario sea un administrador
    if not hasattr(request.user, 'administrador'):
        messages.error(request, 'No tiene permisos para acceder a esta página')
        return redirect('base')
    
    # Tu lógica para el panel de administración
    return render(request, 'panel_administrador.html')


def login_administrador(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Autenticar al usuario
        user = authenticate(request, email=email, password=password)

        if user is not None and isinstance(user, Administrador):
            login(request, user)
            return redirect('panel_administrador')
        else:
            messages.error(request, 'Credenciales inválidas o no tiene permisos de administrador')

    return render(request, 'base.html')  # Vuelve a la página base




