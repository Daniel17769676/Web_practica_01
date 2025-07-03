from django.db import models

class Servicio (models.Model):    
    nombre = models.CharField(max_length=100, unique =True) #esto sirve para que no se repitan los nombres de los servicios
    descripcion = models.TextField(blank=True, null=True) #este campos permite que la descripcion sea opcional
    duracion = models.DurationField() #esto permite que la duracion sea un campo de tipo duracion
    activo = models.BooleanField(default=True) #esto permite que el servicio este activo o no

    #La linea DEF __str__ permite que al imprimir el objeto se muestre el nombre del servicio
    def __str__(self):
        return self.nombre
    
    
    class Meta:
        verbose_name = 'Servicio' #Este campo permite que se muestre el nombre del modelo en singular en el panel de administracion
        verbose_name_plural = 'Servicios' #Este campo permite que se muestre el nombre del modelo en plural en el panel de administracion

class HorariosDisponibles (models.Model):
    DIA_SEMANA_CHOICES = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ] #La LISTA anterior permite que se muestren los dias de la semana en el panel de administracion, el que se guarda en la base de datos como un numero del 0 al 6

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='horarios_disponibles') #esto permite que se relacione el servicio con los horarios disponibles
    dia_semana = models.IntegerField(choices=DIA_SEMANA_CHOICES) #este campo permite que se guarde el dia de la semana como un numero del 0 al 6
    hora_inicio = models.TimeField() #este campo permite que se guarde la hora de inicio del horario disponible
    hora_fin = models.TimeField() #este campo permite que se guarde la hora de fin del horario disponible
    disponible = models.BooleanField(default=True) #este campo permite que el horario este disponible o no

    #La linea DEF __str__ permite que al imprimir el objeto se muestre el dia de la semana, la hora de inicio y la hora de fin
    def __str__(self):
        return f"{self.get_dia_semana_display()} ({self.hora_inicio} - {self.hora_fin}) - {self.servicio.nombre}"
    
    class Meta:
        verbose_name = 'Horario Disponible' #Este campo permite que se muestre el nombre del modelo en singular en el panel de administracion
        verbose_name_plural = 'Horarios Disponibles' #Este campo permite que se muestre
        unique_together = ('servicio', 'dia_semana', 'hora_inicio', 'hora_fin') #esto permite que no se repitan los horarios disponibles para el mismo servicio en el mismo dia de la semana

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]  # Esta lista permite que se muestren los estados de la reserva en el panel de administracion

    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT) #esto permite que se relacione la reserva con el servicio
    fecha = models.DateField() #este campo permite que se guarde la fecha de la reserva
    hora_inicio = models.TimeField() #este campo permite que se guarde la hora de inicio de la reserva
    hora_fin = models.TimeField() #este campo permite que se guarde la hora de
    cliente_nombre = models.CharField(max_length=100) #este campo permite que se guarde el nombre del cliente
    cliente_email = models.EmailField() #este campo permite que se guarde el email del cliente
    observaciones = models.TextField(blank=True, null=True) #este campo permite que se guarden las observaciones de la reserva
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente') #este campo permite que se guarde el estado de la reserva
    fecha_creacion = models.DateTimeField(auto_now_add=True) #este campo permite que se guarde la fecha de creacion de la reserva
    fecha_actualizacion = models.DateTimeField(auto_now=True) #este campo permite que se guarde la fecha de actualizacion de la reserva
    cliente_telefono = models.CharField(max_length=15, blank=True, null=True) #este campo permite que se guarde el telefono del cliente, es opcional

    
    def __str__(self):
        return f"Reserva #{self.id}-{self.cliente_nombre} ({self.servicio.nombre} - {self.fecha})"
    
    class Meta:
        verbose_name = 'Reserva' #Este campo permite que se muestre el nombre del modelo en singular en el panel de administracion
        verbose_name_plural = 'Reservas' #Este campo permite que se muestre el nombre del modelo en plural en el panel de administracion
        ordering = ['-fecha', '-hora_inicio'] #esto permite que las reservas se ordenen por fecha y hora de inicio, de mas reciente a mas antiguo


