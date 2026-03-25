from django.urls import path
from .views import *


urlpatterns = [
    path("", index, name="index"),
    path("horarios/", horarios_disponiveis, name="horarios"),
    path("meus-agendamentos/", historico, name="meus-agendamentos"),
    path("cancelar/<int:id>/", cancelar_agendamento, name="cancelar"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("verificar-descanso/", verificar_descanso, name="verificar_descanso")
]