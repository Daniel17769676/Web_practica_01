from django.contrib import admin
from .models import Administrador, Disponibilidad

# Registra los modelos en el admin de Django
admin.site.register(Administrador)
admin.site.register(Disponibilidad)

