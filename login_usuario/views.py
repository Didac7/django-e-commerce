from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate

@csrf_exempt
def login_usuario(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            return JsonResponse({'message': 'Login exitoso', 'username': user.username})
        else:
            return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)