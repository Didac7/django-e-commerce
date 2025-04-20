from rest_framework import serializers
from .models import Cliente, Usuario, Categoria, Producto, Carrito, DetalleCarrito, Pedido, DetallePedido, Pago, Envio

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

# class UsuarioRegistroSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(write_only=True)

#     class Meta:
#         model = Usuario  # Usamos tu modelo Usuario
#         fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

#     def validate(self, data):
#         if data['password'] != data['password2']:
#             raise serializers.ValidationError("Las contraseñas no coinciden.")
#         return data

#     def create(self, validated_data):
#         validated_data.pop('password2')  # No guardamos 'password2'
#         usuario = Usuario.objects.create_user(**validated_data)
#         return usuario

class UsuarioRegistroSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # No guardamos 'password2'
        usuario = Usuario.objects.create_user(**validated_data)
        return usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    
    class Meta:
        model = Producto
        fields = '__all__'

class DetalleCarritoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')
    producto_precio = serializers.ReadOnlyField(source='producto.precio')
    
    class Meta:
        model = DetalleCarrito
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    detalles = DetalleCarritoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Carrito
        fields = '__all__'

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')
    
    class Meta:
        model = DetallePedido
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pedido
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class EnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envio
        fields = '__all__'