from django.urls import path
from .views import *


urlpatterns = [
    path("meu-perfil/", meu_perfil, name="meu-perfil"),
    path("criar-conta/", criar_conta, name="criar_conta"),
]