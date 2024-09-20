from django.db import models

# Crear tus modelos aquí. (Los modelos son tablas de la base de datos)
   
class Reserva(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    cargo = models.CharField(max_length=100)
    email = models.EmailField()
    fecha = models.DateField()
    hora = models.TimeField()   

    def __str__(self):
        return f"{self.nombre} - {self.fecha} - {self.hora}"


