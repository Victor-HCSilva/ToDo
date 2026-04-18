from django.shortcuts import render
from home.models import Todo, User, Image
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from home.forms import TodoForm, ImageForm
from todo.utils import (
    get_label,
    clean_dict,
    adjust_boolean_fields,
)
from agenda.models import Colors
from django.utils.dateparse import parse_date


@login_required
def anotacoes(request, id_user):
    if request.user.id != id_user:
        return redirect("home:login")

    prazo_inicial = request.GET.get("prazo_inicial", "2025-01-01")
    prazo_final = request.GET.get("prazo_final", "2026-01-01")
    prazo_inicial = parse_date(prazo_inicial)
    prazo_final = parse_date(prazo_final)

    filters = {
        "tag": request.GET.get("tag", None),
        "prioridade": get_label(request.GET.get("prioridade", None)),
        "favorito": request.GET.get("favorito", None),
        "completo": request.GET.get("completo", None),
        "titulo__icontains": request.GET.get("titulo", None),
        "user": get_object_or_404(User, id=id_user),
        "is_active": True,
    }

    if filters.get("user", None) is None:
        return redirect("home:login")

    filters = clean_dict(filters)
    filters = adjust_boolean_fields(filters)
    todos = Todo.objects.filter(**filters).order_by("-id")
    cor_obj = Colors.objects.filter(user=filters["user"]).first()
    cor_de_destaque = cor_obj.cor_de_destaque if cor_obj else "#3273dc"

    context = {
        "anotacoes": todos,
        "all_tags": Todo.TAGS,
        "all_prioridades": Todo.PRIORIDADES,
        "selected_tag": filters.get("tag"),
        "selected_prioridade": filters.get("prioridade"),
        "selected_favorito": filters.get("favorito"),
        "selected_completo": filters.get("completo"),
        "selected_titulo": request.GET.get("titulo", ""),
        "cor_de_destaque": cor_de_destaque,
        "prazo_inicial": prazo_inicial,
        "prazo_final": prazo_final,
    }

    return render(request, "anotacoes.html", context)


@login_required()
def show(request, id_user, id_anotacao):
    form = ImageForm()

    if request.user.id != id_user:
        return redirect("home:login")
    task = get_object_or_404(Todo, id=id_anotacao)
    user = get_object_or_404(User, id=id_user)

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = get_object_or_404(Todo, id=id_anotacao)
            image.save()

    imgs = Image.objects.filter(user=get_object_or_404(Todo, id=id_anotacao))

    context = {
        "tarefa": task,
        "user": user,
        "form": form,
        "imagens": imgs,
    }
    return render(request, "show.html", context)


@login_required()
def editar(request, id_user, id_anotacao):
    if request.user.id != id_user:
        return redirect("home:login")

    todo = get_object_or_404(Todo, id=id_anotacao)
    user = get_object_or_404(User, id=id_user)
    form = TodoForm(instance=todo)

    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        todo = form.save(commit=False)
        todo.user = user
        todo.save()
        return redirect("home:anotacoes", id_user=id_user)

    context = {
        "user": user,
        "form": form,
        "tarefa": todo,
    }
    return render(request, "editar.html", context)


@login_required()
def remover(request, id_user, id_anotacao):
    if request.user.id != id_user:
        return redirect("home:login")
    todo = get_object_or_404(Todo, id=id_anotacao)
    user = get_object_or_404(User, id=id_user)

    if request.method == "POST":
        todo.is_active = False
        todo.save()
        return redirect("home:anotacoes", id_user=id_user)
    else:
        return render(request, "delete.html", {"user": user, "tarefa": todo})


@login_required()
def apagar_imagem(request, id_user, id_imagem, id_anotacao):
    image = get_object_or_404(Image, id=id_imagem)
    user = get_object_or_404(User, id=id_user)
    todo = get_object_or_404(Todo, id=id_anotacao)
    form = ImageForm(instance=image)

    if request.user.id != id_user:
        return redirect("home:login")

    if request.method == "POST":
        image.delete()
        return redirect("home:show", id_user=id_user, id_anotacao=id_anotacao)
    else:
        print(form.errors)
    return render(
        request, "apagar_imagem.html", {"user": user, "imagem": image, "tarefa": todo}
    )


@login_required()
def editar_descricao(request, id_user, id_imagem, id_anotacao):
    image = get_object_or_404(Image, id=id_imagem)
    user = get_object_or_404(User, id=id_user)
    todo = get_object_or_404(Todo, id=id_anotacao)
    form = ImageForm(request.POST, request.FILES, instance=image)

    # Consertar com o login_required
    if request.user.id != id_user:
        return redirect("home:login")

    if request.method == "POST":
        image = form.save(commit=False)
        image.user = todo
        image.save()
        return redirect("home:show", id_user=id_user, id_anotacao=id_anotacao)

    context = {"user": user, "imagem": image, "tarefa": todo, "form": form}
    return render(request, "editar_descricao.html", context)


def not_found(request):
    return render(request, "404.html")
