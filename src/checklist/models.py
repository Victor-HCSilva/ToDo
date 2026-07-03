from django.contrib.auth.models import User
from django.db import models

from checklist.configs.colors import COLORS


class Tarefa(models.Model):
    titulo = models.CharField(max_length=100)
    color = models.CharField(max_length=20, choices=COLORS, default="black")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo}"


class Item(models.Model):
    # Correção da sintaxe das tuplas de escolhas (choices)
    STATUS_CHOICES = [
        ("nao_iniciado", "⮟ Não Iniciado ⚪"),
        ("fazendo", "⮟ Fazendo ⏳"),
        ("concluido", "⮟ Concluído ✅"),
        ("cancelado", "⮟ Cancelado 🚫"),
    ]

    descricao = models.CharField(max_length=255, default="Item da lista")
    feito = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="nao_iniciado"
    )
    color = models.CharField(max_length=20, choices=COLORS, default="black")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="itens")
    tarefa = models.ForeignKey(
        Tarefa, on_delete=models.CASCADE, related_name="itens", blank=True, null=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        tarefa_titulo = self.tarefa.titulo if self.tarefa else "Sem tarefa"
        return f"{self.descricao} (Tarefa: {tarefa_titulo}) - {self.user.username}"


class Link(models.Model):
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="links")
    tarefa = models.ForeignKey(
        Tarefa, on_delete=models.CASCADE, related_name="links", blank=True, null=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.url}"
