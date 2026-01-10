from django.shortcuts import render
from app.init.models import Todo, User, Image
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from app.init.forms import TodoForm, ImageForm
from app.main.utils import (
    get_time_diff_days,
    get_label,
    clean_dict,
    adjust_boolean_fields,
)
from app.agenda.models import Colors
from django.utils.dateparse import parse_date


@login_required
def anotacoes(request, id_user):
    # Garantir que o usuário só veja suas próprias anotações
    if request.user.id != id_user:
        return redirect('main:login')

    # Obter datas de filtro, com defaults seguros
    prazo_inicial = request.GET.get('prazo_inicial', '2025-01-01')
    prazo_final = request.GET.get('prazo_final', '2026-01-01')

    # Converter para objetos de data (evita falhas no filtro)
    prazo_inicial = parse_date(prazo_inicial)
    prazo_final = parse_date(prazo_final)

    # Montagem dos filtros dinâmicos
    filters = {
        "tag": request.GET.get('tag', None),
        "prioridade": get_label(request.GET.get('prioridade', None)),
        "favorito": request.GET.get('favorito', None),
        "completo": request.GET.get('completo', None),
        "titulo__icontains": request.GET.get('titulo', None),
        "user": get_object_or_404(User, id=id_user),
        "is_active": True,
    }

    if filters.get("user", None) is None:
        return redirect('main:login')

    # Apenas adiciona o range se as datas forem válidas
    # if prazo_inicial and prazo_final:
    #     filters["prazo_inicial__range"] = [prazo_inicial, prazo_final]

    # Limpa campos vazios e ajusta booleanos

    filters =  clean_dict(filters)
    filters = adjust_boolean_fields(filters)

    print("Filters:\n", filters)
    
    todos = Todo.objects.filter(
        **filters
    ).order_by("-id")
    # todos = Todo.objects.filter(user=get_object_or_404(User, id=id_user))

    print(
        f"Todos: {todos}"
    )
    # Cor de destaque personalizada do usuário
    cor_obj = Colors.objects.filter(user=filters["user"]).first()
    cor_de_destaque = cor_obj.cor_de_destaque if cor_obj else "#3273dc"

    context = {
        "anotacoes": todos,
        "all_tags": Todo.TAGS,
        "all_prioridades": Todo.PRIORIDADES,
        "selected_tag": filters.get('tag'),
        "selected_prioridade": filters.get('prioridade'),
        "selected_favorito": filters.get('favorito'),
        "selected_completo": filters.get('completo'),
        "selected_titulo": request.GET.get('titulo', ''),
        "cor_de_destaque": cor_de_destaque,
        "prazo_inicial": prazo_inicial,
        "prazo_final": prazo_final,
    }

    return render(request, "anotacoes.html", context)


@login_required()
def show(request, id_user,id_anotacao):
    form = ImageForm()

    if request.user.id != id_user:
        return redirect("main:login")
    task = get_object_or_404(Todo, id=id_anotacao)
    user = get_object_or_404(User, id=id_user)

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            # Atribuindo a imagem a anotação correta
            image.user = get_object_or_404(Todo, id=id_anotacao)
            image.save()
        else:
            print("Errors:", form.errors)

    imgs = Image.objects.filter(user=get_object_or_404(Todo, id=id_anotacao))
    context = {
        "tarefa":task,
        "user": user,
        "form":form,
        "imagens": imgs,
    }
    return render(request, "show.html", context)


@login_required()
def editar(request, id_user, id_anotacao):
    #Consertar com o login_required
    if request.user.id != id_user:
        return redirect('main:login')

    todo = get_object_or_404(Todo, id=id_anotacao)
    user = get_object_or_404(User, id=id_user)
    form = TodoForm(instance=todo)

    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        todo = form.save(commit=False)
        todo.user = user
        todo.save()
        return redirect("main:anotacoes", id_user=id_user)
    else:
        print(form.errors)

    context = {
        "user": user,
        "form": form,
        "tarefa": todo,
    }
    return render (request, "editar.html", context)


@login_required()
def remover(request, id_user, id_anotacao):
    if request.user.id != id_user:
        return redirect('main:login')

    todo = get_object_or_404(Todo, id=id_anotacao)
    user = get_object_or_404(User, id=id_user)
    form = TodoForm(instance=todo)

    if request.method == "POST":
        todo.is_active = False
        todo.save()
        return redirect("main:anotacoes", id_user=id_user)
    else:
        print("Erros no formulario: ", form.errors)
        return render (request, "delete.html", {"user":user, "tarefa":todo})


@login_required()
def apagar_imagem(request, id_user, id_imagem,id_anotacao):
    image = get_object_or_404(Image, id=id_imagem)
    user = get_object_or_404(User, id=id_user)
    todo = get_object_or_404(Todo, id=id_anotacao)

    form = ImageForm(instance=image)

    #Consertar com o login_required
    if request.user.id != id_user:
        return redirect('main:login')

    if request.method == "POST":
        image.delete()
        return redirect("main:show", id_user=id_user, id_anotacao=id_anotacao)
    else:
        print(form.errors)
    return render (request, "apagar_imagem.html", {"user":user, "imagem":image, "tarefa":todo})


@login_required()
def editar_descricao(request, id_user, id_imagem, id_anotacao):
    image = get_object_or_404(Image, id=id_imagem)
    user = get_object_or_404(User, id=id_user)
    todo = get_object_or_404(Todo, id=id_anotacao)
    form = ImageForm(request.POST, request.FILES, instance=image)

    #Consertar com o login_required
    if request.user.id != id_user:
        return redirect('main:login')

    if request.method == "POST":
        image = form.save(commit=False)
        image.user = todo
        image.save()
        return redirect("main:show", id_user=id_user, id_anotacao=id_anotacao)
    else:
        print(form.errors)

    context = {
        "user":user,
        "imagem":image,
        "tarefa":todo,
        "form":form
    }
    return render (request, "editar_descricao.html", context)

def not_found(request):
    return render(request, "404.html")
