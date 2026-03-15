from django.db import models
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

    quadra = models.ForeignKey(Quadra, on_delete=models.SET_NULL, null=True, blank=True)
    horario = models.ForeignKey(Horario, on_delete=models.SET_NULL, null=True, blank=True)

    quadra_nome = models.CharField(max_length=255, blank=True, null=True)
    quadra_numero = models.IntegerField(null=True, blank=True)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fim = models.TimeField(null=True, blank=True)

    data = models.DateField(null=True, blank=True)


    class Meta:
        unique_together = ('quadra', 'horario', 'data')

    def __str__(self):
        return f'{self.usuario}'


class Descanso(models.Model):

    DIAS_SEMANA = [
        ("seg", "Segunda"),
        ("ter", "Terça"),
        ("qua", "Quarta"),
        ("qui", "Quinta"),
        ("sex", "Sexta"),
        ("sab", "Sábado"),
        ("dom", "Domingo"),
    ]

    dias_semana = models.JSONField(blank=True, null=True)

    def __str__(self):
        if not self.dias_semana:
            return "Arena aberta todos os dias"

        dias = dict(self.DIAS_SEMANA)
        nomes = [dias[d] for d in self.dias_semana if d in dias]

        return "Descanso: " + ", ".join(nomes)