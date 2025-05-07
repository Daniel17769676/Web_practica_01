from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Disponibilidad
from .forms import DisponibilidadForm

# Vista para GESTIONAR disponibilidades (administradores)
class GestionDisponibilidadView(CreateView):
    model = Disponibilidad
    form_class = DisponibilidadForm
    template_name = 'servicios/gestion_disponibilidad.html'
    success_url = '/servicios/disponibilidad/'

# Vista para LISTAR disponibilidades (usuarios)
class ListaDisponibilidadView(ListView):
    model = Disponibilidad
    template_name = 'servicios/lista_disponibilidad.html'
    context_object_name = 'disponibilidades'

    def get_queryset(self):
        fecha = self.request.GET.get('fecha')
        if fecha:
            return Disponibilidad.objects.filter(dia=fecha)
        return Disponibilidad.objects.all()
    
def disponibilidad_view(request):
    return render(request, 'mi_web/Disponibilidad.html')