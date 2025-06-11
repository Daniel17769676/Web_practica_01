from django.db import models

# Crear tus modelos aquí. (Los modelos son tablas de la base de datos)

# Modelo para los administradores
class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()

    class Meta:
        db_table = 'ADMINISTRADOR'  # Nombre de la tabla en la base de datos

    def __str__(self):
        return self.nombre

# Modelo para la disponibilidad de los administradores
class Disponibilidad(models.Model):
    DIAS_CHOICES = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miércoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sábado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]
    administrador = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    servicio = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True, verbose_name="Disponible para reserva")

    class Meta:
        db_table = 'DISPONIBILIDAD'
    
    def __str__(self):
        # Obtiene los días relacionados y los une en un string
        dias = ", ".join([dia.get_dia_display() for dia in self.dias.all()])
        return f'{self.administrador} - {dias} ({self.hora_inicio}-{self.hora_fin}) {"✅" if self.disponible else "❌"}'
    
class ServicioDia(models.Model):
    OPCIONES_DIAS= [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miércoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sábado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]
    
    disponibilidad = models.ForeignKey(
        'Disponibilidad', 
        on_delete=models.CASCADE,
        related_name='dias'  # Permite acceder con `disponibilidad.dias.all()`
    )
    dia = models.CharField(max_length=9, choices=OPCIONES_DIAS)
    
    class Meta:
        db_table = 'SERVICIO_DIA'  # Nombre de la tabla en Oracle
        verbose_name = 'Día del servicio'
        verbose_name_plural = 'Días del servicio'
    
    def get_dia_display(self):
        """Devuelve la etiqueta legible del día (ej. 'Lunes' en lugar de 'lunes')"""
        return dict(self.OPCIONES_DIAS).get(self.dia, self.dia)
    
    def __str__(self):
        return f'{self.disponibilidad.servicio} - {self.get_dia_display()}'