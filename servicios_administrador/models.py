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
    dia = models.CharField(max_length=9, choices=DIAS_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    servicio = models.CharField(max_length=100)

    disponible = models.BooleanField(default=True, verbose_name="Disponible para reserva")

    class Meta:
        db_table = 'DISPONIBILIDAD'
    
    def __str__(self):
        return f'{self.administrador} - {self.dia} ({self.hora_inicio}-{self.hora_fin}) {"✅" if self.disponible else "❌"}'
    
class Reserva(models.Model):
    administrador = models.ForeignKey('Administrador', on_delete=models.CASCADE)  # Relación con el administrador
    disponibilidad = models.ForeignKey('Disponibilidad', on_delete=models.CASCADE)  # Relación con disponibilidad
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)

    class Meta:
        db_table = 'RESERVA' # Nombre de la tabla en la base de datos

    def __str__(self):
        return f'Reserva para {self.nombre} - {self.disponibilidad.dia}'
