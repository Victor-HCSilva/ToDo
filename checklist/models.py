"""
A tarefa tem o nome principal

o item tem a descrição - label - passível a mudar para descricao
o item tem vinculo unico de user e link, formando um conjunto separado de itens e links por user
o link é separado para que possa ser atribuido a tarefa ou (o caso de agora) o item; onde a url precisa ter um vinculo fiel a tarefa e a um usuário

A escolha de como as entidades se juntam muda o formato de exibição, criação e edição dos dados; portanto,
também muda a forma como os dados são armazenados no banco de dados. Logo penso que existem abordagens melhores ou inferiores
"""

from django.contrib.auth.models import User
from django.db import models

from checklist.configs.colors import COLORS


class Tarefa(models.Model):
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
        Tarefa, on_delete=models.CASCADE, related_name="itens", blank=True, null=True
    )

    def __str__(self):
        return f"{self.label} - {self.user.username}"


class Links(models.Model):
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Itens, on_delete=models.CASCADE, related_name="links")

    def __str__(self):
        return f"{self.url} - {self.user.username}"
