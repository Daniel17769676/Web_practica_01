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
    INTERVALO_CHOICES = [
        (15, '15 minutos'),
        (30, '30 minutos'),
        (60, '1 hora'),
    ]

    administrador = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    servicio = models.CharField(max_length=100)
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
    
    def __str__(self):
        dias = ", ".join([dia.get_dia_display() for dia in self.dias.all()])
        intervalo = f"({self.intervalo} min)" if not self.es_franja_maestra else ""
        return f'{self.administrador} - {dias} ({self.hora_inicio}-{self.hora_fin}) {intervalo} {"✅" if self.disponible else "❌"}'
    
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