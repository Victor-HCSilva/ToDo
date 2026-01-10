from datetime import date

def get_time_diff_days(data_inicial: date, data_final: date) -> int:
    """Calcula a diferença em dias entre dois objetos date."""
    diferenca = data_final - data_inicial
    return diferenca.days


def get_time_remainder(data_final: date) -> int:
    """Calcula os dias restantes data final - data incial inicial"""
    data_inicial = date.today()
    diferenca = data_final - data_inicial
    return diferenca.days


def get_label(level: str) -> str | None: 
    """Niveis de importância na tarefa"""
    levels = {
        "1": "Mínima",
        "2": "Mediana",
        "3": "Máxima",
    }
    return levels.get(level, None)

def clean_dict(filters: dict) -> dict:
    """Retira campo vazios dos filtros"""
    for k, v in filters.copy().items():
        if v is None or v == '' or not v:
            filters.pop(k)
    return filters

def adjust_boolean_fields(filters: dict) -> dict:
    """Ajuste para campos boleanos: 
    'true' -> True
    'false' -> False
    """
    bolean_fields = ["favorito", "completo"]
    for k, v in filters.copy().items():
        if k in bolean_fields:
            if v in ["true", 1, "1"]:
                filters[k] = True
            else:
                filters[k] = False
    return filters


if __name__ == "__main__":
    # Testes
    import os
    import django
    import sys

# 1️⃣ Adicione a raiz do projeto ao sys.path (para garantir que 'core' seja encontrado)
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))  # ./

# 2️⃣ Defina a variável de ambiente do settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# 3️⃣ Inicialize o Django
    django.setup()

    from app.init.models import Todo

    s = Todo.objects.all()
    for i in s:
        # print(i.message(), i.prazo_dias, i.prazo_inicial, i.prazo_final)
        print(
            f"{i.message()}\nDias restantes: {i.prazo_dias}\n\
Prazo inicial: {i.prazo_inicial} \nPrazo final: {i.prazo_final}"
        )
