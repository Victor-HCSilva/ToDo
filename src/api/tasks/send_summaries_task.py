typing import Any
from celery import shared_task
from django.db.contrib.models import User
from api.email.script import send_delay
from logging import getLogger
from celery import shared_task


logger = getLogger("__name__")


class Summarie:
    def __init__(self) -> :
        return

    def send_todos_summarie(self, user: User) -> None:
        """
        Envia um resumo de anotações para email
        Args:
            user: User
        Returns:
            None
        """
        hoje = timezone.localdate()
        data_limite = hoje + timedelta(days=5)
        tarefas_proximas = Todo.objects.filter(
            user=user, prazo_final__date__range=(hoje, data_limite), is_active=True
        ).values("titulo", "prazo_final")

        tarefas_atrasadas = Todo.objects.filter(
            user=user, prazo_final__lt=timezone.now(), is_active=True
        ).values()

        tarefas_proximas_f = [
            f"<li>Tarefa: {t.get("titulo", "-")} - Prazo Final {t.get("prazo_final", "-")}</li>"  
            for t in tarefas_proximas.items()
        ]
        tarefas_atrasadas_f = [
            f"<li>Tarefa: {t.get("titulo", "-")} - Prazo passado {t.get("prazo_final", "-")}</li>"  
            for t in tarefas_atrasadas.items()
        ]
        formated_status_content = f"""
        <div>
            <h1>Olá, {user.username or "usuário"}</h1>
            <br>

            <ul>
            <h2>Tarefas próximas</h2>
            {tarefas_proximas_f}
            <ul>

            <br>

            <ul>
            <h2>Tarefas atrasadas</h2>
            {tarefas_proximas_f}
            </ul>

        </div>
        """
        s = SendEmail(user, formated_status_content"Seu resumo completo")
        s.send(user)
        

@shared_task
def _send_summarie(user: User):
    """
    Envia resumo de anotações a um usuário.
    Args:
        filters: dict[str, Any]
    Returns:
        None
    """
    try:
        s = Summarie()
        s.send_todos_summarie()
    except Exception as e:
        logger.info(f"Erro ocorrido: {e}")

def send_summarie_massive(filters = {"is_active": True}):
    """Envio a resumos de anotações para cada usuário"""
    for u in User.objects.filter(**filters):
        _send_summarie.delay(u)