from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.contrib.auth import authenticate

# @csrf_exempt
# def login_usuario(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username = data.get('username')
#         password = data.get('password')
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             return JsonResponse({'message': 'Login exitoso', 'username': user.username})
#         else:
#             return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
#     else:
#         return JsonResponse({'error': 'Método no permitido'}, status=405)






# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.contrib.auth import authenticate
# from django.contrib.auth import get_user_model

# User = get_user_model()  # ← Esto carga tu modelo personalizado (Usuario de tienda)

# @csrf_exempt
# def login_usuario(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username = data.get('username')
#         password = data.get('password')
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             return JsonResponse({
#                 'message': 'Login exitoso',
#                 'username': user.username,
#                 'rol': user.rol  # ← Devolvemos el rol desde tu modelo personalizado
#             })
#         else:
#             return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
#     else:
#         return JsonResponse({'error': 'Método no permitido'}, status=405)







from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()  # Esto carga tu modelo personalizado (Usuario de tienda)

# @csrf_exempt
# def login_usuario(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username = data.get('username')
#         password = data.get('password')
#         print(f"Recibido: username={username}, password={password}")
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             # Verificar si el usuario es administrador
#             print(f"Usuario autenticado: {user.username}, Rol: {user.rol}")
#             is_admin = user.rol == 'ADMIN'
#             cliente_id = user.cliente.id if hasattr(user, 'cliente') else None
#             print(f"Es admin: {is_admin}")
#             return JsonResponse({
#                 'message': 'Login exitoso',
#                 'username': user.username,
#                 'rol': user.rol,
#                 'is_admin': is_admin,  # Devolvemos si es administrador
#                 'cliente_id': cliente_id
#                 #'cliente_id': user.cliente.id if hasattr(user, 'cliente') else None
#             })
#         else:
#             print("Credenciales inválidas")
#             return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
#     else:
#             print("Método no permitido")
#             return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def login_usuario(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            print(f"Recibido: username={username}, password={password}")
            user = authenticate(username=username, password=password)

            if user is not None:
                print(f"Usuario autenticado: {user.username}, Rol: {user.rol}")
                is_admin = user.rol == 'ADMIN'

                try:
                    cliente_id = user.cliente.id
                except Exception:
                    cliente_id = None

                print(f"Es admin: {is_admin}")
                return JsonResponse({
                    'message': 'Login exitoso',
                    'username': user.username,
                    'rol': user.rol,
                    'is_admin': is_admin,
                    'cliente_id': cliente_id
                })
            else:
                print("Credenciales inválidas")
                return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)