from django.db import models
from agendamento.settings import AUTH_USER_MODEL

class Fatura(models.Model):
    titulo = models.CharField(max_length=255, null=True, blank=True)
    cliente = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    valor = models.DecimalField(decimal_places=2, max_digits=10)
    referencia = models.CharField(max_length=50, null=True, blank=True)
    data_vencimento = models.DateField(null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'Referência: {self.referencia} vencimento: {self.data_vencimento}'