from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Item, Link, Tarefa


@login_required
def checklist(request):
    # Processamento de envio de formulários rápidos
    if request.method == "POST":
        # AÇÃO 1: Criar uma nova Tarefa (apenas com o título)
        if "criar_tarefa" in request.POST:
            titulo = request.POST.get("titulo")
            color = request.POST.get("color", "black")
            if titulo:
                Tarefa.objects.create(titulo=titulo, color=color, user=request.user)
            return redirect("checklist")

        # AÇÃO 2: Adicionar um Item rápido diretamente a uma Tarefa existente
        elif "adicionar_item" in request.POST:
            descricao = request.POST.get("descricao")
            tarefa_id = request.POST.get("tarefa_id")
            if descricao and tarefa_id:
                tarefa_obj = get_object_or_404(Tarefa, id=tarefa_id, user=request.user)
                Item.objects.create(
                    descricao=descricao, tarefa=tarefa_obj, user=request.user
                )
            return redirect("checklist")

        # AÇÃO 3: Adicionar um Link rápido diretamente a uma Tarefa existente
        elif "adicionar_link" in request.POST:
            url = request.POST.get("url")
            tarefa_id = request.POST.get("tarefa_id")
            if url and tarefa_id:
                tarefa_obj = get_object_or_404(Tarefa, id=tarefa_id, user=request.user)
                Link.objects.create(url=url, tarefa=tarefa_obj, user=request.user)
            return redirect("checklist")

    # Carrega os dados do usuário para exibição organizada
    tarefas = Tarefa.objects.filter(user=request.user).prefetch_related(
        "itens", "links"
    )

    return render(request, "checklist.html", {"tarefas": tarefas})
