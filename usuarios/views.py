from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])  # 👈 PERMITE ACCESO A USUARIOS NO AUTENTICADOS
def login_usuario(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        return Response({'message': 'Login exitoso', 'username': user.username}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
    
@api_view(['POST'])
def registrar_usuario(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Se requieren username y password'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'El usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'Usuario creado exitosamente'}, status=status.HTTP_201_CREATED)