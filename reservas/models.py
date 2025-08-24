from django.db import models


class Reserva(models.Model):    
    disponibilidad = models.ForeignKey('servicios.Disponibilidad', on_delete=models.PROTECT, related_name='reservas') #esto permite que se relacione la reserva con la disponibilidad    
    fecha_reserva = models.DateField() #este campo permite que se guarde la fecha de la reserva
    horario = models.CharField(max_length=50) #este campo permite que se guarde el horario de la reserva
    cliente_nombre = models.CharField(max_length=100) #este campo permite que se guarde el nombre del cliente
    cliente_rut = models.CharField(max_length=20, blank=False, null=False) #este campo permite que se guarde el rut del cliente, es obligatorio
    cliente_telefono = models.CharField(max_length=15, blank=True, null=True) #este campo permite que se guarde el telefono del cliente, es opcional
    cliente_email = models.EmailField() #este campo permite que se guarde el email del cliente
    observaciones = models.TextField(blank=True, null=True) #este campo permite que se guarden las observaciones de la reserva    
    ESTADO_CHOICES = [     
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente') #este campo permite que se guarde el estado de la reserva   
    
    def __str__(self):
        return f"Reserva #{self.id}-{self.cliente_nombre} ({self.disponibilidad.servicio.nombre} - {self.fecha_reserva})"
    
    class Meta:
        verbose_name = 'Reserva' #Este campo permite que se muestre el nombre del modelo en singular en el panel de administracion
        verbose_name_plural = 'Reservas' #Este campo permite que se muestre el nombre del modelo en plural en el panel de administracion
        ordering = ['fecha_reserva'] #esto permite que las reservas se ordenen por fecha y hora de inicio, de mas reciente a mas antiguocls
