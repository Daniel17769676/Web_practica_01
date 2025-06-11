from django.forms import ModelForm
from servicios.models import Disponibilidad, Reserva

class ReservaForm(ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre', 'email', 'telefono', 'disponibilidad']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disponibilidad'].queryset = Disponibilidad.objects.filter(disponible=True)
        self.fields['disponibilidad'].widget.attrs.update({'class': 'form-control'})