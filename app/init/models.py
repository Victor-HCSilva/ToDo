from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from app.main.utils import get_time_diff_days, get_time_remainder

class Todo(models.Model):
    TAGS = [
        ("Universidade.","Universidade"),
        ("Casa","Casa"),
        ("Urgente.","Urgente"),
        ("Importante.","Importante"),
        ("Tarefa.","Tarefa"),
        ("Lembrete.","Lembrete"),
        ("Avulso","Avulso"),
        ("Outro","Outro"),
    ]
    PRIORIDADES = [
        ("Mínima", "1"),
        ("Mediana","2"),
        ("Máxima", "3"),
    ]
    user = models.ForeignKey(
            User,
            on_delete=models.CASCADE
    )
    titulo = models.CharField(
        max_length=200,
        default="Sem titulo"
    )
    favorito = models.BooleanField(
        default=False
    )
    completo = models.BooleanField(
        default=False
    )
    anotacao = models.TextField(
        ("Anotação"),
        default="Escreva algo aqui!"
    )
    prioridade = models.CharField(
        choices=PRIORIDADES,
        max_length=10,
        default="1"
    )
    tag = models.CharField(
        choices=TAGS,
        max_length=13,
        default=("Avulso","Avulso")
    )
    prazo_inicial = models.DateField(
        default=timezone.now,
        help_text=f'eg. {str(timezone.now().date())}'
    )
    prazo_final = models.DateField(
        default=timezone.now,
        help_text=f'eg. {str(timezone.now().date())}'
    )
    is_active = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(("Data de Criação"), auto_now_add=True)
    updated_at = models.DateTimeField(("Data de Atualização"), auto_now=True)


    @property
    def prazo_dias(self):
        if self.prazo_final:
            return get_time_remainder(self.prazo_final)
        return None

    def message(self):
        if self.prazo_dias is None:
            return ""
        return "Passou do prazo: " if self.prazo_dias <= 0 else "Dias restantes: "

    @property
    def color(self):
        match self.prazo_dias:
            case None:
                return "gray"
            case x if x >= 7:
                return "#00ff00"
            case x if 3 <= x < 7:
                return "orange"
            case x if 1 <= x <= 2:
                return "violet"
            case _:
                return "#b82b14"

    def __str__(self):
        return (f"Titulo: {self.titulo}")


class Image(models.Model):
    img = models.ImageField(
        upload_to="imgs"
    )
    descricao = models.CharField(
        max_length=1000,
        default="Imagem sem descriçao"
    )
    titulo = models.CharField(
        max_length=1000, default="Sem titulo"
    )
    data_de_criacao = models.DateField(
        default=timezone.now
    )
    #Cada user tem um todo relacionado
    user = models.ForeignKey(
        Todo,
        on_delete=models.CASCADE,
        related_name="imagem"
    )
    observacao = models.CharField(max_length=1000, default="Sem observação")

    def __str__(self):
        return f"Titulo: {self.titulo} - {self.data_de_criacao}"
