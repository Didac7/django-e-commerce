from rest_framework import serializers
from .models import Cliente, Usuario, Categoria, Producto, Carrito, DetalleCarrito, Pedido, DetallePedido, Pago, Envio

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class UsuarioRegistroSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'rol']
    
    # Validación para asegurar que las contraseñas coinciden
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    # Crear el usuario, y si es necesario, crear un Cliente si el rol es CLIENTE
    def create(self, validated_data):
        validated_data.pop('password2')  # No guardamos 'password2'
        rol = validated_data.get('rol', 'USER')  # Asignamos 'USER' como rol por defecto

        # Si el rol es 'CLIENTE', creamos un cliente relacionado
        if rol == 'USER':
            cliente = Cliente.objects.create(
                nombre=validated_data.get('first_name', '') + ' ' + validated_data.get('last_name', ''),
                email=validated_data['email'],
                direccion="Dirección por defecto"
            )
            validated_data['cliente'] = cliente  # Asociamos el cliente al usuario

        # Creamos el usuario usando el método `create_user` de Django
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
        #fields = '__all__'
        fields = ['id', 'nombre', 'descripcion']

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    #imagen = serializers.ImageField(required=False)
    #imagen = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = '__all__'

    # def get_imagen(self, obj):
    #     request = self.context.get('request')
    #     if obj.imagen:
    #         imagen_url = obj.imagen.url
    #         if request is not None:
    #             return request.build_absolute_uri(imagen_url)
    #         return imagen_url
    #     return None

    def create(self, validated_data):
        imagen = self.context['request'].FILES.get('imagen')
        if imagen:
            validated_data['imagen'] = imagen
        return super().create(validated_data)

    def update(self, instance, validated_data):
        imagen = self.context['request'].FILES.get('imagen')
        if imagen:
            validated_data['imagen'] = imagen
        return super().update(instance, validated_data)

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