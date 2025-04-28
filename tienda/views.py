from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework import status
from .models import Cliente, Usuario, Categoria, Producto, Carrito, DetalleCarrito, Pedido, DetallePedido, Pago, Envio
from .serializers import (ClienteSerializer, UsuarioSerializer, CategoriaSerializer, ProductoSerializer,
                          CarritoSerializer, DetalleCarritoSerializer, PedidoSerializer, DetallePedidoSerializer,
                          PagoSerializer, EnvioSerializer, UsuarioRegistroSerializer )
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]  # Permitir acceso público para leer categorías

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]  # Solo admin puede modificar
        return super().get_permissions()

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]  # Permitir acceso público para ver productos

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context   

    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'partial_update', 'destroy']:
    #         return [IsAdminUser()]  # Solo admin puede modificar
    #     #return super().get_permissions()
    #     return [AllowAny()]
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        categoria_id = request.query_params.get('categoria_id')
        if categoria_id:
            productos = Producto.objects.filter(categoria_id=categoria_id)
            serializer = self.get_serializer(productos, many=True)
            return Response(serializer.data)
        return Response({"error": "Categoría no especificada"}, status=400)

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filtrar carritos solo del usuario actual
        cliente_id = self.request.query_params.get('cliente_id')
        if cliente_id:
            return Carrito.objects.filter(cliente_id=cliente_id)
        return Carrito.objects.none()

class DetalleCarritoViewSet(viewsets.ModelViewSet):
    queryset = DetalleCarrito.objects.all()
    serializer_class = DetalleCarritoSerializer
    permission_classes = [IsAuthenticated]

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Para clientes normales, solo ver sus propios pedidos
        cliente_id = self.request.query_params.get('cliente_id')
        if cliente_id and not self.request.user.is_staff:
            return Pedido.objects.filter(cliente_id=cliente_id)
        # Para administradores, ver todos los pedidos
        if self.request.user.is_staff:
            return Pedido.objects.all()
        return Pedido.objects.none()

class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    permission_classes = [IsAuthenticated]

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated]

class EnvioViewSet(viewsets.ModelViewSet):
    queryset = Envio.objects.all()
    serializer_class = EnvioSerializer
    permission_classes = [IsAuthenticated]

# class RegistroUsuarioAPIView(APIView):
#     permission_classes = [AllowAny]  # Permitimos acceso público al registro
    
#     def post(self, request):
#         serializer = UsuarioRegistroSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Usuario registrado con éxito"}, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistroUsuarioAPIView(CreateAPIView):
    serializer_class = UsuarioRegistroSerializer
    permission_classes = [AllowAny]  # Permite que cualquier persona registre un usuario sin estar autenticado

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
