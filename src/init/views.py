from axes.models import AccessAttempt  # Importe o modelo do Axes
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import FolderForm, TodoForm, UserForm
from .models import Folder, Todo


def home(request):
    if not request.user.is_authenticated:
        return redirect("main:login")
    return render(request, "home.html")


@login_required()
def create_todo(request, id_user: int):
    filters = {
        "user": get_object_or_404(User, id=id_user, is_active=True),
        "is_active": True,
    }
    folders = Folder.objects.filter(**filters)
    todos = Todo.objects.filter(**filters)
    form = TodoForm()
    user = get_object_or_404(User, id=id_user)

    if request.user.id != id_user:
        return redirect("login")

    if request.method == "POST":
        form = TodoForm(request.POST)
        todo = form.save(commit=False)
        todo.user = user
        todo.save()
        return redirect("main:anotacoes", id_user=id_user)

    context = {
        "username": user.username.title(),
        "todos": todos,
        "form": form,
        "folders": folders,
    }
    return render(request, "main.html", context)


@login_required()
def welcome(request, id_user):
    if request.user.id != id_user:
        return redirect("main:login")

    user = get_object_or_404(User, id=id_user, is_active=True)
    todos = Todo.objects.filter(user=user, is_active=True)
    context = {
        "nick": "nick",
        "todos": todos,
        "user": user,
    }
    return render(request, "welcome.html", context)


def sobre(request):
    if not request.user.is_authenticated:
        raise Http404("Página não encontrada")
    user = get_object_or_404(User, id=request.user.id)
    return render(request, "sobre.html", {"user": user})


def create_account(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, "new_account.html", {"form": form})

    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(username=username, password=password)
            if user.id:
                return redirect(reverse_lazy("main:login"))
        else:
            return render(request, "new_account.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy("main:welcome", kwargs={"id_user": self.request.user.id})

    def form_invalid(self, form):
        username = self.request.POST.get("username")

        # Consultamos quantas tentativas falhas existem para este usuário
        # O Axes filtra isso pelo 'username' ou 'user_agent' ou 'ip_address'
        attempts = AccessAttempt.objects.filter(username=username).count()

        limit = 5  # O mesmo limite que você definiu no settings
        remaining = limit - attempts

        if remaining > 0:
            messages.error(
                self.request,
                f"Usuário ou senha inválidos. Você possui {remaining} tentativa(s) restante(s).",
            )
        else:
            messages.error(
                self.request,
                "Conta bloqueada por excesso de tentativas. Tente novamente em 5 minutos.",
            )

        return super().form_invalid(form)


@login_required
def folder_list_create(request):
    # Lista apenas as pastas ativas do usuário logado
    folders = Folder.objects.filter(user=request.user, is_active=True)

    if request.method == "POST":
        form = FolderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]

            # 1. Verifica se já existe uma pasta ativa com este nome
            if Folder.objects.filter(
                user=request.user, name=name, is_active=True
            ).exists():
                messages.error(request, "Você já possui uma pasta ativa com este nome.")
            else:
                # 2. Verifica se existe uma pasta deletada (inativa) com este nome para reativar
                inactive_folder = Folder.objects.filter(
                    user=request.user, name=name, is_active=False
                ).first()
                if inactive_folder:
                    inactive_folder.is_active = True
                    inactive_folder.save()
                    messages.success(request, f"Pasta '{name}' reativada com sucesso!")
                else:
                    # 3. Cria uma nova pasta normalmente
                    folder = form.save(commit=False)
                    folder.user = request.user
                    folder.save()
                    messages.success(request, f"Pasta '{name}' criada com sucesso!")
                return redirect("main:folders")
    else:
        form = FolderForm()

    return render(request, "folders.html", {"folders": folders, "form": form})


@login_required
def folder_update(request, folder_id):
    # Recupera apenas se estiver ativa e pertencer ao usuário logado
    folder = get_object_or_404(Folder, id=folder_id, user=request.user, is_active=True)

    if request.method == "POST":
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            name = form.cleaned_data["name"]
            # Evita duplicidade com outra pasta ativa
            if (
                Folder.objects.filter(user=request.user, name=name, is_active=True)
                .exclude(id=folder_id)
                .exists()
            ):
                messages.error(
                    request, "Você já possui outra pasta ativa com este nome."
                )
            else:
                form.save()
                messages.success(request, "Pasta atualizada com sucesso!")
                return redirect("main:folders")
    else:
        form = FolderForm(instance=folder)

    return render(request, "folder_edit.html", {"form": form, "folder": folder})


@login_required
def folder_delete(request, folder_id):

    folder = get_object_or_404(Folder, id=folder_id, user=request.user, is_active=True)
    if request.method == "POST":
        folder.is_active = False
        folder.save()
        messages.success(
            request, f"Pasta '{folder.name}' movida para a lixeira (removida)."
        )
    return redirect("main:folders")
