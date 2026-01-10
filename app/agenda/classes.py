import calendar
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import ColorForm
from django.contrib.auth.models import User
from .models import Colors, AgendaModel
from .forms import AgendaForm
from collections import defaultdict


class Agenda:
    def __init__(self, request):
        self.request = request

    def agenda(self, id_user, ano=None, mes=None):
        if self.request.user.id != id_user:
            return redirect('main:login')

        form = AgendaForm(self.request.POST or None) # Use 'or None' para GET requests
        user = get_object_or_404(User, id=id_user)

        if self.request.method == "POST":
            if form.is_valid():
                agenda = form.save(commit=False)
                agenda.user = user
                agenda.save()
                # Redireciona para o mesmo mês/ano do evento criado
                return redirect("agenda:eventos",
                                id_user=id_user,)
            else:
                print("Erros no formulário:", form.errors)

        # Lógica do Calendário
        agora = datetime.now()
        # Usa o ano/mês da URL, ou o atual como padrão
        ano_visualizado = ano or agora.year
        mes_visualizado = mes or agora.month

        cal = calendar.Calendar(firstweekday=6) # Domingo como primeiro dia
        mes_dias = cal.monthdayscalendar(ano_visualizado, mes_visualizado)
        nome_mes = calendar.month_name[mes_visualizado]

        # Busca a cor de configuração do usuário
        cor_obj = Colors.objects.filter(user=user).first()
        cor_de_destaque = cor_obj.cor_de_destaque if cor_obj else "#3273dc" # Um azul padrão se não houver
        #print(cor_de_destaque)
        # Busca eventos e agrupa por dia
        eventos_do_mes = AgendaModel.objects.filter(
            user=user,
            dia_do_evento__year=ano_visualizado,
            dia_do_evento__month=mes_visualizado
        ).order_by('dia_do_evento__time') # Ordena por hora do dia

        eventos_por_dia = defaultdict(list)
        for evento in eventos_do_mes:
            eventos_por_dia[evento.dia_do_evento.day].append(evento.titulo)

        context = {
            'form': form,
            'id_user': id_user,
            'ano': ano_visualizado,
            'mes': mes_visualizado,
            'nome_mes': nome_mes,
            'dias_semana': ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
            'mes_dias': mes_dias,
            'cor_de_destaque': cor_de_destaque,
            'eventos_por_dia': dict(eventos_por_dia),

            # --- Adições Cruciais ---
            # Envia a data atual REAL para o template
            "dia_atual": agora.day,
            "mes_atual": agora.month,
            "ano_atual": agora.year,
        }

        return render(self.request, "agenda.html", context)


class Eventos():
    def __init__(self, request: HttpRequest):
        self.request = request

    def eventos_(self,  id_user: int):
        user = get_object_or_404(User, id=id_user)
        eventos = AgendaModel.objects.filter(
            user=user,
            is_active=True
        )
        for i in eventos:
            print("eventos:  ", i.importancia , "  ---- ", "tipo: -- ", type(i.importancia))
        context = {
            "eventos":eventos,
            "user":user,
        }
        return render(self.request, "eventos.html",context)

    def detalhe_sobre_evento(self,  id_user: int, id_evento):
        user = get_object_or_404(User, id=id_user)
        evento = get_object_or_404(AgendaModel,id=id_evento)
        context = {
            "evento":evento,
            "user":user,
        }

        return render(self.request, "detalhe_sobre_evento.html",context)


class Configs:
    def __init__(self, request: HttpRequest):
        self.request = request


    def configs(self, id_user: int):
        #Caso não seja o mesmo usuario
        if self.request.user.id != id_user:
            return redirect('main:login')

        form = ColorForm(self.request.POST)
        user = get_object_or_404(User, id=id_user)
        context = {
            "nada":"nada",
            "cor_de_destaque":form,
            "user":user,
        }

        if self.request.method == "POST":
            if form.is_valid():
                config = form.save(commit=False)
                config.user = user
                print("User:",config.user)
                config.save()
                return redirect("agenda:agenda", id_user=id_user)
        else:
            print("Erros",form.errors)

        return render(self.request, "configs.html", context)


class DeleteOrEditEvent():
    def __init__(self, request: HttpRequest):
        self.request = request


    def delete_event(self, id_user: int, id_event):
        #Caso não seja o mesmo usuario
        if self.request.user.id != id_user:
            return redirect('main:login')

        evento = get_object_or_404(AgendaModel, id=id_event)
        user = get_object_or_404(User, id=id_user)
        context = {
            "user":user,
            "evento":evento,
        }

        if self.request.method == "POST":
            evento.is_active = False
            evento.save()
            return redirect("agenda:eventos", id_user=id_user)

        return render(self.request, "delete_event.html", context)


    def edit_event(self, id_user: int, id_event: int):
        #Caso não seja o mesmo usuario
        if self.request.user.id != id_user:
            return redirect('main:login')

        evento = get_object_or_404(AgendaModel, id=id_event)
        user = get_object_or_404(User, id=id_user)

        if self.request.method == "POST":
            form = AgendaForm(self.request.POST, instance=evento)
            if form.is_valid():
                form.save()
            else:
                print("erros",form.errors)

            return redirect("agenda:eventos", id_user=id_user)

        form = AgendaForm(instance=evento)
        context = {
            "nada":"nada",
            "form":form,
            "user":user,
        }

        return render(self.request, "edit.html", context)
