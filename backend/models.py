from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    cpf = models.CharField(max_length=20, unique=True)
    data_nasc = models.DateField(null=True, blank=True)
    telefone = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.cpf}"


class Quadra(models.Model):
    numeracao = models.IntegerField(blank=True, null=True)
    apelido = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.apelido} - {self.numeracao}'


class Horario(models.Model):
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    def __str__(self):
        return f'{self.hora_inicio} - {self.hora_fim}'


class Agendamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    quadra = models.ForeignKey(Quadra, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    data = models.DateField()

    class Meta:
        unique_together = ('quadra', 'horario', 'data')

    def __str__(self):
        return f'{self.usuario}'