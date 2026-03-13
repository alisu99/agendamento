from django.urls import path
from . import views

urlpatterns = [
    path("pix/<int:agendamento_id>/", views.pagar_pix, name="pagar_pix"),
    path("webhook/mercadopago/", views.webhook_mercadopago),
]
