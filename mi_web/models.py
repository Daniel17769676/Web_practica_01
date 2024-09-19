from django.db import models
from django.contrib.auth.models import User

# Crear tus modelos aquí. (Los modelos son tablas de la base de datos)

class Usuario(models.Model):
    user = models.CharField(max_length=50, verbose_name="usuario")
    nombre = models.CharField(max_length=50, verbose_name="nombre")
    email = models.EmailField(max_length=50, verbose_name="email")
    password = models.CharField(max_length=50, verbose_name="password")

    def __str__(self):
        return self.user
    
from django.db import models

class Reserva(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    cargo = models.CharField(max_length=100)
    email = models.EmailField()
    fecha = models.DateField()
    hora = models.TimeField()   

    def __str__(self):
        return f"{self.nombre} - {self.fecha} - {self.hora}"


