from django.db import models


class ReservaUsuarios(models.Model):
    administrador = models.ForeignKey('servicios_administrador.Administrador', on_delete=models.CASCADE)  # Relación con el administrador
    disponibilidad = models.ForeignKey('servicios_administrador.Disponibilidad', on_delete=models.CASCADE)  # Relación con disponibilidad
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)

    class Meta:
        db_table = 'RESERVA_USUARIOS' # Nombre de la tabla en la base de datos

    def __str__(self):
        return f'Reserva para {self.nombre} - {self.disponibilidad.dia}'

