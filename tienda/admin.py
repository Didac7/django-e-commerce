from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Cliente, Usuario, Categoria, Producto, Carrito, DetalleCarrito
from .models import Pedido, DetallePedido, Pago, Envio

# Registra tus modelos
admin.site.register(Cliente)
admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(DetalleCarrito)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Pago)
admin.site.register(Envio)