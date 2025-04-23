from django.urls import path
from .views import login_usuario

urlpatterns = [
    path('', login_usuario),
    # path('login/', login_usuario),
]