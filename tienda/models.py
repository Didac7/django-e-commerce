from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(null=False)

    def __str__(self):
        return self.nombre

# class Usuario(models.Model):
#     ROLES = [
#         ('ADMIN', 'Administrador'),
#         ('CLIENTE', 'Cliente'),
#         ('VENDEDOR', 'Vendedor'),
#     ]
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
#     username = models.CharField(max_length=50, unique=True, null=False)
#     password = models.CharField(max_length=255, null=False)  # En producción usar hash
#     rol = models.CharField(max_length=20, choices=ROLES, null=False)

#     def __str__(self):
#         return self.username


class Usuario(AbstractUser):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('CLIENTE', 'Cliente'),
        ('VENDEDOR', 'Vendedor'),
    ]

    rol = models.CharField(max_length=20, choices=ROLES, null=False)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, null=True, blank=True)

    # Ya tienes username, password, email, etc. por herencia

    def __str__(self):
        return self.username

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    stock = models.PositiveIntegerField(null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Carrito de {self.cliente.nombre}"

class DetalleCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(null=False)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class Pedido(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('ENVIADO', 'Enviado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, null=False)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(null=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class Pago(models.Model):
    METODOS_PAGO = [
        ('TARJETA', 'Tarjeta de Crédito/Débito'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('PAYPAL', 'PayPal'),
        ('EFECTIVO', 'Efectivo'),
    ]
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, null=False)

    def __str__(self):
        return f"Pago de ${self.monto} para pedido #{self.pedido.id}"

class Envio(models.Model):
    ESTADOS_ENVIO = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_TRANSITO', 'En Tránsito'),
        ('ENTREGADO', 'Entregado'),
        ('DEVUELTO', 'Devuelto'),
    ]
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    direccion_envio = models.TextField(null=False)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    estado_envio = models.CharField(max_length=20, choices=ESTADOS_ENVIO, null=False)

    def __str__(self):
        return f"Envío para pedido #{self.pedido.id}"