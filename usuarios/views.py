from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from servicios_administrador.models import Disponibilidad
from .forms import ReservaForm

class ReservaView(CreateView):
    form_class = ReservaForm
    template_name = 'usuarios/reservar.html'
    success_url = '/usuarios/reserva-exito/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disponibilidades'] = Disponibilidad.objects.filter(disponible=True)
        return context
    
class ReservaExitoView(TemplateView):
    template_name = 'usuarios/reserva_exito.html'