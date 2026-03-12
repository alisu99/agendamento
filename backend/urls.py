from django.urls import path
from .views import *


urlpatterns = [
    path("meu-perfil/", meu_perfil, name="meu-perfil"),
    path("criar-conta/", criar_conta, name="criar_conta"),
    path("usuarios/", usuarios, name="usuarios"),
    path("novo-usuario", novo_usuario, name="novo-usuario"),
    path("editar-usuario/<int:id>", editar_usuario, name="editar-usuario"),
    path("excluir-usuario/<int:id>", excluir_usuario, name="excluir-usuario"),
    path("agendamentos/", agendamentos, name="agendamentos"),
    path("ajustes/", ajustes, name="ajustes"),
]