from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.models.mixins import ActivableAndTimeStamp


# Cor de destaque
class Colors(ActivableAndTimeStamp):
    class Cor(models.TextChoices):
        AZUL = "blue", "Azul"
        VERDE = "green", "Verde"
        VERMELHO = "red", "Vermelho"
        PRETO = "black", "Preto"
        BRANCO = "#FFFFFF", "Branco"  # Nota: Texto branco pode ficar invisível em fundos claros

        # Tons vibrantes e comuns
        AMARELO = "#FFC107", "Amarelo"
        LARANJA = "orange", "Laranja"  # Mantive "orange" para simplicidade
        ROXO = "#6f42c1", "Roxo"
        ROSA = "#d63384", "Rosa"
        CIANO_TURQUESA = "#0dcaf0", "Ciano/Turquesa"

        # Tons neutros e terrosos
        CINZA = "#6c757d", "Cinza"
        MARROM = "#795548", "Marrom"

        # Tons metálicos
        DOURADO = "#FFD700", "Dourado"
        PRATA = "#C0C0C0", "Prata"

    # OneToOneField garante que cada usuário tenha apenas uma configuração
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True, # Torna o usuário a chave primária da tabela
    )
    cor_de_destaque = models.CharField(
        "Cor de destaque",
        max_length=19,
        choices=Cor.choices,
        default=Cor.AZUL
    )
    cor_do_dia = models.CharField(
        "Cor de destaque",
        max_length=19,
        choices=Cor.choices,
        default=Cor.AZUL
    )

    def __str__(self):
        return f"Configuração de {self.user.username}"




# Agenda
class AgendaModel(ActivableAndTimeStamp):
    PRIORIDADES = [
        ("1","Mínima"),
        ("2","Mediana"),
        ("3","Máxima"),
    ]
    TIPOS_DE_EVENTO = [
        ("Prova","Prova"),
        ("Atividade","Atividade"),
        ("Terefa","Tarefa"),
        ("Importante","Importante"),
        ("Lembrete","Lembrete"),
        ("Outro","Outro"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário"
    )
    titulo = models.CharField("Título", max_length=100, default="Sem titulo")
    descricao = models.TextField("Descrição", blank=True, default="Sem descrição",max_length=100)
    tipo_de_evento = models.CharField(
        "Tipo de Evento",
        max_length=20,
        choices=TIPOS_DE_EVENTO,
        default=TIPOS_DE_EVENTO[4]
    )
    importancia = models.CharField(
        "Importância",
        max_length=2,
        choices=PRIORIDADES,
        default=PRIORIDADES[0],
    )
    dia_do_evento = models.DateTimeField("Data do evento", default=timezone.now)
   


    class Meta:
        ordering = ['dia_do_evento']


    def __str__(self):
        return f"{self.titulo} ({self.user.username}) - {self.dia_do_evento.strftime('%d/%m/%Y')}"
