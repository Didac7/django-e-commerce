from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ClienteViewSet, UsuarioViewSet, CategoriaViewSet, ProductoViewSet,
                    CarritoViewSet, DetalleCarritoViewSet, PedidoViewSet, DetallePedidoViewSet,
                    PagoViewSet, EnvioViewSet, RegistroUsuarioAPIView)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'carritos', CarritoViewSet)
router.register(r'detalles-carrito', DetalleCarritoViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles-pedido', DetallePedidoViewSet)
router.register(r'pagos', PagoViewSet)
router.register(r'envios', EnvioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('registro/', RegistroUsuarioAPIView.as_view(), name='registro_usuario'),  # Ruta para registrar usuario
    path('registrar/', RegistroUsuarioAPIView.as_view(), name='registrar_usuario'),
]