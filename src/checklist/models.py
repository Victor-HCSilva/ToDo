from django.db import models
from checklist.configs.colors import COLORS
from django.contrib.auth.models import User


class Titulo(models.Model):
    titulo = models.CharField(max_length=100)
    color = models.CharField(max_length=20, choices=COLORS, default="black")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} - {self.user.username}"


class Itens(models.Model):
    label = models.CharField(max_length=255, default="Tarefa")
    feito = models.BooleanField(default=False)
    color = models.CharField(max_length=20, choices=COLORS, default="black")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.ForeignKey(
        Titulo, on_delete=models.CASCADE, related_name="itens", blank=True, null=True
    )

    def __str__(self):
        return f"{self.label} - {self.user.username}"
