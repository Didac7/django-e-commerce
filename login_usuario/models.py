from django.db import models

# Create your models here.

# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class UsuarioPersonalizado(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('USER', 'Usuario'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='USER')

    def __str__(self):
        return f"{self.username} ({self.rol})"