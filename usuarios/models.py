# usuarios/models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'ADMINISTRADOR'
        managed = True  # ✅ Django gestionará la tabla
    
    def __str__(self):
        return self.nombre
    
    # 🔐 MÉTODOS PARA MANEJO SEGURO DE CONTRASEÑAS
    def set_password(self, raw_password):
        """Hashea y guarda la contraseña"""
        self.password = make_password(raw_password)
        self.save()
    
    def check_password(self, raw_password):
        """Verifica si la contraseña en texto plano coincide con el hash almacenado"""
        return check_password(raw_password, self.password)
    
    # Métodos adicionales para compatibilidad
    def get_username(self):
        return self.correo
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False