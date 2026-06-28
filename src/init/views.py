# from axes.models import AccessAttempt  # Importe o modelo do Axes
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.contrib.auth.views import LoginView
# from django.http import Http404
# from django.shortcuts import get_object_or_404, redirect, render
# from django.urls import reverse_lazy
# from django.utils.dateparse import parse_date

# from agenda.models import Colors
# from init.forms import ImageForm, TodoForm
# from init.models import Folder, Image, Todo
# from main.utils import (
#     adjust_boolean_fields,
#     clean_dict,
#     get_label,
# )

# from .forms import FolderForm, UserForm


# def home(request):
#     if not request.user.is_authenticated:
#         return redirect("main:login")
#     return render(request, "home.html")


# @login_required()
# def create_todo(request, id_user: int):
#     filters = {
#         "user": get_object_or_404(User, id=id_user, is_active=True),
#         "is_active": True,
#     }
#     folders = Folder.objects.filter(**filters)
#     todos = Todo.objects.filter(**filters)
#     form = TodoForm()
#     user = get_object_or_404(User, id=id_user)

#     if request.user.id != id_user:
#         return redirect("login")

#     if request.method == "POST":
#         form = TodoForm(request.POST)
#         todo = form.save(commit=False)
#         todo.user = user
#         todo.save()
#         return redirect("main:anotacoes", id_user=id_user)

#     context = {
#         "username": user.username.title(),
#         "todos": todos,
#         "form": form,
#         "folders": folders,
#     }
#     return render(request, "main.html", context)


# @login_required()
# def welcome(request, id_user):
#     if request.user.id != id_user:
#         return redirect("main:login")

#     user = get_object_or_404(User, id=id_user, is_active=True)
#     todos = Todo.objects.filter(user=user, is_active=True)
#     context = {
#         "nick": "nick",
#         "todos": todos,
#         "user": user,
#     }
#     return render(request, "welcome.html", context)


# def sobre(request):
#     if not request.user.is_authenticated:
#         raise Http404("Página não encontrada")
#     user = get_object_or_404(User, id=request.user.id)
#     return render(request, "sobre.html", {"user": user})


# def create_account(request):
#     if request.method == "GET":
#         form = UserForm()
#         return render(request, "new_account.html", {"form": form})

#     elif request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]

#             user = User.objects.create_user(username=username, password=password)
#             if user.id:
#                 return redirect(reverse_lazy("main:login"))
#         else:
#             return render(request, "new_account.html", {"form": form})


# class CustomLoginView(LoginView):
#     template_name = "login.html"

#     def get_success_url(self):
#         return reverse_lazy("main:welcome", kwargs={"id_user": self.request.user.id})

#     def form_invalid(self, form):
#         username = self.request.POST.get("username")

#         # Consultamos quantas tentativas falhas existem para este usuário
#         # O Axes filtra isso pelo 'username' ou 'user_agent' ou 'ip_address'
#         attempts = AccessAttempt.objects.filter(username=username).count()

#         limit = 5  # O mesmo limite que você definiu no settings
#         remaining = limit - attempts

#         if remaining > 0:
#             messages.error(
#                 self.request,
#                 f"Usuário ou senha inválidos. Você possui {remaining} tentativa(s) restante(s).",
#             )
#         else:
#             messages.error(
#                 self.request,
#                 "Conta bloqueada por excesso de tentativas. Tente novamente em 5 minutos.",
#             )

#         return super().form_invalid(form)


# @login_required
# def folder_list_create(request):
#     # Lista apenas as pastas ativas do usuário logado
#     folders = Folder.objects.filter(user=request.user, is_active=True)

#     if request.method == "POST":
#         form = FolderForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data["name"]

#             # 1. Verifica se já existe uma pasta ativa com este nome
#             if Folder.objects.filter(
#                 user=request.user, name=name, is_active=True
#             ).exists():
#                 messages.error(request, "Você já possui uma pasta ativa com este nome.")
#             else:
#                 # 2. Verifica se existe uma pasta deletada (inativa) com este nome para reativar
#                 inactive_folder = Folder.objects.filter(
#                     user=request.user, name=name, is_active=False
#                 ).first()
#                 if inactive_folder:
#                     inactive_folder.is_active = True
#                     inactive_folder.save()
#                     messages.success(request, f"Pasta '{name}' reativada com sucesso!")
#                 else:
#                     # 3. Cria uma nova pasta normalmente
#                     folder = form.save(commit=False)
#                     folder.user = request.user
#                     folder.save()
#                     messages.success(request, f"Pasta '{name}' criada com sucesso!")
#                 return redirect("main:folders")
#     else:
#         form = FolderForm()

#     return render(request, "folders.html", {"folders": folders, "form": form})


# @login_required
# def folder_update(request, folder_id):
#     # Recupera apenas se estiver ativa e pertencer ao usuário logado
#     folder = get_object_or_404(Folder, id=folder_id, user=request.user, is_active=True)

#     if request.method == "POST":
#         form = FolderForm(request.POST, instance=folder)
#         if form.is_valid():
#             name = form.cleaned_data["name"]
#             # Evita duplicidade com outra pasta ativa
#             if (
#                 Folder.objects.filter(user=request.user, name=name, is_active=True)
#                 .exclude(id=folder_id)
#                 .exists()
#             ):
#                 messages.error(
#                     request, "Você já possui outra pasta ativa com este nome."
#                 )
#             else:
#                 form.save()
#                 messages.success(request, "Pasta atualizada com sucesso!")
#                 return redirect("main:folders")
#     else:
#         form = FolderForm(instance=folder)

#     return render(request, "folder_edit.html", {"form": form, "folder": folder})


# @login_required
# def folder_delete(request, folder_id):

#     folder = get_object_or_404(Folder, id=folder_id, user=request.user, is_active=True)
#     if request.method == "POST":
#         folder.is_active = False
#         folder.save()
#         messages.success(
#             request, f"Pasta '{folder.name}' movida para a lixeira (removida)."
#         )
#     return redirect("main:folders")


# @login_required
# def anotacoes(request, id_user):
#     if request.user.id != id_user:
#         return redirect("main:login")

#     prazo_inicial = request.GET.get("prazo_inicial", "2025-01-01")
#     prazo_final = request.GET.get("prazo_final", "2026-01-01")
#     prazo_inicial = parse_date(prazo_inicial)
#     prazo_final = parse_date(prazo_final)

#     # Coleta a pasta selecionada no filtro
#     selected_folder = request.GET.get("folder", None)
#     if selected_folder and selected_folder.isdigit():
#         selected_folder = int(
#             selected_folder
#         )  # Converte para int para bater com o ID no template

#     filters = {
#         "tag": request.GET.get("tag", None),
#         "prioridade": get_label(request.GET.get("prioridade", None)),
#         "favorito": request.GET.get("favorito", None),
#         "completo": request.GET.get("completo", None),
#         "titulo__icontains": request.GET.get("titulo", None),
#         "folder_id": selected_folder,  # Filtro por ID da pasta
#         "user": get_object_or_404(User, id=id_user),
#         "is_active": True,
#     }

#     if filters.get("user", None) is None:
#         return redirect("main:login")

#     filters = clean_dict(filters)
#     filters = adjust_boolean_fields(filters)

#     # Busca todas as anotações baseadas nos filtros
#     todos = Todo.objects.filter(**filters).order_by("-id")

#     # Busca todas as pastas ativas do usuário logado para carregar no dropdown do filtro
#     folders = Folder.objects.filter(user=filters["user"], is_active=True)

#     cor_obj = Colors.objects.filter(user=filters["user"]).first()
#     cor_de_destaque = cor_obj.cor_de_destaque if cor_obj else "#3273dc"

#     context = {
#         "anotacoes": todos,
#         "folders": folders,  # Passa as pastas para o template
#         "all_tags": Todo.TAGS,
#         "all_prioridades": Todo.PRIORIDADES,
#         "selected_tag": filters.get("tag"),
#         "selected_prioridade": filters.get("prioridade"),
#         "selected_favorito": filters.get("favorito"),
#         "selected_completo": filters.get("completo"),
#         "selected_folder": selected_folder,  # Passa a pasta selecionada de volta para o filtro
#         "selected_titulo": request.GET.get("titulo", ""),
#         "cor_de_destaque": cor_de_destaque,
#         "prazo_inicial": prazo_inicial,
#         "prazo_final": prazo_final,
#     }

#     return render(request, "anotacoes.html", context)


# @login_required()
# def show(request, id_user, id_anotacao):
#     form = ImageForm()

#     if request.user.id != id_user:
#         return redirect("main:login")
#     task = get_object_or_404(Todo, id=id_anotacao)
#     user = get_object_or_404(User, id=id_user)

#     if request.method == "POST":
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             image = form.save(commit=False)
#             image.user = get_object_or_404(Todo, id=id_anotacao)
#             image.save()

#     imgs = Image.objects.filter(user=get_object_or_404(Todo, id=id_anotacao))

#     context = {
#         "tarefa": task,
#         "user": user,
#         "form": form,
#         "imagens": imgs,
#     }
#     return render(request, "show.html", context)


# @login_required()
# def editar(request, id_user, id_anotacao):
#     if request.user.id != id_user:
#         return redirect("main:login")

#     todo = get_object_or_404(Todo, id=id_anotacao)
#     user = get_object_or_404(User, id=id_user)
#     form = TodoForm(instance=todo)

#     if request.method == "POST":
#         form = TodoForm(request.POST, instance=todo)
#         todo = form.save(commit=False)
#         todo.user = user
#         todo.save()
#         return redirect("main:anotacoes", id_user=id_user)

#     context = {
#         "user": user,
#         "form": form,
#         "tarefa": todo,
#     }
#     return render(request, "editar.html", context)


# @login_required()
# def remover(request, id_user, id_anotacao):
#     if request.user.id != id_user:
#         return redirect("main:login")
#     todo = get_object_or_404(Todo, id=id_anotacao)
#     user = get_object_or_404(User, id=id_user)

#     if request.method == "POST":
#         todo.is_active = False
#         todo.save()
#         return redirect("main:anotacoes", id_user=id_user)
#     else:
#         return render(request, "delete.html", {"user": user, "tarefa": todo})


# @login_required()
# def apagar_imagem(request, id_user, id_imagem, id_anotacao):
#     image = get_object_or_404(Image, id=id_imagem)
#     user = get_object_or_404(User, id=id_user)
#     todo = get_object_or_404(Todo, id=id_anotacao)
#     form = ImageForm(instance=image)

#     if request.user.id != id_user:
#         return redirect("main:login")

#     if request.method == "POST":
#         image.delete()
#         return redirect("main:show", id_user=id_user, id_anotacao=id_anotacao)
#     else:
#         print(form.errors)
#     return render(
#         request, "apagar_imagem.html", {"user": user, "imagem": image, "tarefa": todo}
#     )


# @login_required()
# def editar_descricao(request, id_user, id_imagem, id_anotacao):
#     image = get_object_or_404(Image, id=id_imagem)
#     user = get_object_or_404(User, id=id_user)
#     todo = get_object_or_404(Todo, id=id_anotacao)
#     form = ImageForm(request.POST, request.FILES, instance=image)

#     # Consertar com o login_required
#     if request.user.id != id_user:
#         return redirect("main:login")

#     if request.method == "POST":
#         image = form.save(commit=False)
#         image.user = todo
#         image.save()
#         return redirect("main:show", id_user=id_user, id_anotacao=id_anotacao)

#     context = {"user": user, "imagem": image, "tarefa": todo, "form": form}
#     return render(request, "editar_descricao.html", context)


# def not_found(request):
#     return render(request, "404.html")
