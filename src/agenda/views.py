from .classes import Agenda, Configs, DeleteOrEditEvent, Eventos
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required


@login_required()
def agenda(request: HttpRequest, id_user, ano=None, mes=None):
    agenda = Agenda(request)
    return agenda.agenda(id_user=id_user, ano=ano, mes=mes)


@login_required()
def configs_(request: HttpRequest, id_user: int):
    configs = Configs(request=request)
    return configs.configs(id_user=id_user)


@login_required()
def eventos_(request: HttpRequest, id_user: int):
    eventos = Eventos(request=request)
    return eventos.eventos_(id_user=id_user)


@login_required()
def delete_event_(request: HttpRequest, id_user: int, id_event: int):
    delete_event = DeleteOrEditEvent(request=request)
    return delete_event.delete_event(id_user=id_user, id_event=id_event)


@login_required()
def edit_event(request: HttpRequest, id_user: int, id_event: int):
    edit_event = DeleteOrEditEvent(request=request)
    return edit_event.edit_event(id_user=id_user, id_event=id_event)


@login_required()
def detalhe_sobre_evento_(request: HttpRequest, id_user: int, id_evento: int):
    detalhe = Eventos(request=request)
    return detalhe.detalhe_sobre_evento(id_user=id_user, id_evento=id_evento)
