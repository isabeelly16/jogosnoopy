
from django.db import models

class Jogador(models.Model):
    nome = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nome

class Pontuacao(models.Model):
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name="pontuacoes")
    pontuacao = models.PositiveIntegerField(default=0)
    fase = models.PositiveSmallIntegerField(default=1)
    pistas = models.PositiveSmallIntegerField(default=0)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-pontuacao", "-data"]

    def __str__(self):
        return f"{self.jogador.nome} — {self.pontuacao}"
