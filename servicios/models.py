from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.core.validators import MinValueValidator

# Crear tus modelos aquí. (Los modelos son tablas de la base de datos)

# Modelo para la disponibilidad de los administradores
class Disponibilidad(models.Model):
    INTERVALO_CHOICES = [
        (15, '15 minutos'),
        (30, '30 minutos'),
        (60, '1 hora'),
    ]
    administrador = models.CharField(max_length=100)
    fecha_inicio = models.DateField(
        validators=[MinValueValidator(date.today())],  # Asegura que la fecha sea hoy o futura
        verbose_name="Fecha de inicio",  # Nombre legible para el usuario en el admin
    )
    fecha_fin = models.DateField(
        validators=[MinValueValidator(date.today())],  # Asegura que la fecha sea hoy o futura
        verbose_name="Fecha de fin",  # Nombre legible para el usuario en el admin  
    )
    ubicacion = models.CharField(max_length=200, verbose_name="Ubicación del servicio")  # Ubicación donde se presta el servicio
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE, related_name='disponibilidades',
        verbose_name="Servicio asociado") # Relación con el modelo Servicio (AÑADE)
    disponible = models.BooleanField(default=True, verbose_name="Disponible para reserva")
    intervalo = models.PositiveSmallIntegerField(
        choices=INTERVALO_CHOICES, 
        default=30, 
        verbose_name="Duracion de cada turno"
    )
    es_franja_maestra = models.BooleanField(
        default=False,
        verbose_name="¿Es una franja horaria maestra?"
    )
    franja_padre = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='sub_franjas',
        verbose_name="Franja original"
    )

    class Meta:
        db_table = 'DISPONIBILIDAD'
    verbose_name_plural = 'Disponibilidades'

    def get_turnos(self):
        """
        Genera los turnos disponibles basados en hora_inicio, hora_fin e intervalo
        Devuelve una lista de diccionarios con inicio y fin de cada turno
        """
        turnos = []
        hora_actual = datetime.combine(timezone.now().date(), self.hora_inicio)
        hora_fin = datetime.combine(timezone.now().date(), self.hora_fin)
        intervalo = timedelta(minutes=self.intervalo)
        
        while hora_actual + intervalo <= hora_fin:
            turno = {
                'inicio': hora_actual.time(),
                'fin': (hora_actual + intervalo).time()
            }
            turnos.append(turno)
            hora_actual += intervalo
        
        return turnos
    
    def __str__(self):        
        intervalo = f"({self.intervalo} min)" if not self.es_franja_maestra else ""
        return f'{self.administrador} - ({self.hora_inicio}-{self.hora_fin}) {intervalo} {"✅" if self.disponible else "❌"}'
    



class Servicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del servicio")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    duracion = models.DurationField(
    default=timedelta(minutes=30),
        verbose_name="Duración estimada",
        help_text="Duración estándar para este servicio"
        )
    activo = models.BooleanField(
        default=True,
        verbose_name="¿Activo?",
        help_text="Desmarcar para ocultar este servicio"
        )
 
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.duracion})"