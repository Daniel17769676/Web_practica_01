from django import forms
from .models import Disponibilidad, Reserva
from django.forms import ModelForm

# Formulario para gestionar disponibilidades (nuevo)
class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = '__all__'  # O campos específicos: ['dia', 'hora_inicio', 'hora_fin', ...]
        
    # Opcional: Personalizar widgets para campos de fecha/hora
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dia'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['hora_inicio'].widget = forms.TimeInput(attrs={'type': 'time'})
        self.fields['hora_fin'].widget = forms.TimeInput(attrs={'type': 'time'})

# Formulario para reservas (el que ya tienes)
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre', 'email', 'telefono', 'disponibilidad']
    
    disponibilidad = forms.ModelChoiceField(
        queryset=Disponibilidad.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )