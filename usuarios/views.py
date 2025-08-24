from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from reservas.models import Reserva
from usuarios.models import Administrador
from django.contrib.auth.decorators import login_required

# Decorador personalizado para verificar sesión de admin
def admin_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('is_admin_logged_in'):
            messages.error(request, 'Debe iniciar sesión como administrador')
            return redirect('base')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@admin_login_required  # Usa SOLO tu decorador personalizado
def panel_administrador(request):
    # Obtener datos del admin desde la sesión
    admin_id = request.session.get('admin_id')
    
    try:
        admin = Administrador.objects.get(id=admin_id)
    except Administrador.DoesNotExist:
        messages.error(request, 'Administrador no encontrado')
        return redirect('base')
    
    # ✅ CONSULTA DE RESERVAS
    consulta_admin = Reserva.objects.select_related(
        'disponibilidad__servicio'
    ).order_by('-fecha_reserva', '-horario')

    if not consulta_admin.exists():
        messages.info(request, 'No hay reservas registradas.')
    
    # Debug para verificar
    print(f"Reservas encontradas: {consulta_admin.count()}")
    for reserva in consulta_admin:
        print(f"Reserva ID: {reserva.id}, Cliente: {reserva.cliente_nombre}")
    
    context = {
        'admin': admin,
        'reservas': consulta_admin
    }
    
    return render(request, 'usuarios/panel_administrador.html', context)

def login_administrador(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Buscar el administrador por email
            admin = Administrador.objects.get(correo=email)
            
            # 🔐 Verificar contraseña usando el nuevo método
            if admin.check_password(password):
                # Crear variables de sesión
                request.session['admin_id'] = admin.id
                request.session['admin_nombre'] = admin.nombre
                request.session['admin_email'] = admin.correo
                request.session['is_admin_logged_in'] = True
                
                messages.success(request, f'¡Bienvenido {admin.nombre}!')
                return redirect('usuarios:panel_administrador')
            else:
                messages.error(request, 'Contraseña incorrecta')
                
        except Administrador.DoesNotExist:
            messages.error(request, 'No existe un administrador con este email')

    return render(request, 'base.html')

def logout_administrador(request):
    # Limpiar la sesión
    request.session.flush()
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('base')