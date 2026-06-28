from django.contrib.auth.models import User
from django.db import models
from checklist.configs.colors import COLORS
from main.models import Todo


class Tarefa(models.Model):
    titulo = models.CharField(max_length=100)
    color = models.CharField(max_length=20, choices=COLORS, default="black")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.ForeignKey(
        Todo,
        help_text="Tarefa associada | não é obrigatório",
        on_delete=models.CASCADE,
        related_name="tarefas",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.titulo} - {self.user.username}"


class Item(models.Model):
    # Correção da sintaxe das tuplas de escolhas (choices)
    STATUS_CHOICES = [
        ("nao_iniciado", "Não Iniciado"),
        ("fazendo", "Fazendo"),
        ("concluido", "Concluído"),
        ("cancelado", "Cancelado"),
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

    def __str__(self):
        tarefa_titulo = self.tarefa.titulo if self.tarefa else "Sem tarefa"
        return f"{self.descricao} (Tarefa: {tarefa_titulo}) - {self.user.username}"


class Link(models.Model):
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="links")
    tarefa = models.ForeignKey(
        Tarefa, on_delete=models.CASCADE, related_name="links", blank=True, null=True
    )

    def __str__(self):
        return f"{self.url}"
