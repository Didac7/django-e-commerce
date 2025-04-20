from django.urls import path
from .views import login_usuario
from .views import login_usuario, registrar_usuario

urlpatterns = [
    path('login/', login_usuario),
    path('registro/', registrar_usuario),
]