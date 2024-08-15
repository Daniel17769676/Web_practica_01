from django.db import models

# Crear tus modelos aquí. (Los modelos son tablas de la base de datos)

class Usuario(models.Model):
    usuario = models.CharField(max_length=50, verbose_name="usuario")
    nombre = models.CharField(max_length=50, verbose_name="nombre")
    email = models.EmailField(max_length=50, verbose_name="email")
    password = models.CharField(max_length=50, verbose_name="password")

    def __str__(self):
        return self.usuario
    
from django.db import models

class Reserva(models.Model):
    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=100)
    horario = models.DateTimeField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} - {self.horario}"


