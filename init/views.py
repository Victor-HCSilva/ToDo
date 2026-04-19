from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import TodoForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Todo
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


def home(request):
    return render(request, "home.html")


@login_required()
def create_todo(request, id_user: int):
    todos = Todo.objects.filter(user=get_object_or_404(User, id=id_user))
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
    }
    return render(request, "main.html", context)


@login_required()
def welcome(request, id_user):
    if request.user.id != id_user:
        return redirect("main:login")

    user = get_object_or_404(User, id=id_user)
    todos = Todo.objects.filter(user=get_object_or_404(User, id=id_user))
    context = {
        "nick": "nick",
        "todos": todos,
        "user": user,
    }
    return render(request, "welcome.html", context)


def sobre(request):
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
    """
    Uma view de login customizada para redirecionar o usuário para a sua
    página de boas-vindas, que requer o ID do usuário como argumento.
    """

    template_name = "login.html"

    def get_success_url(self):
        """
        Este método é chamado após um login bem-sucedido.
        Ele constrói a URL de redirecionamento dinamicamente.
        """
        user = self.request.user
        return reverse_lazy("main:welcome", kwargs={"id_user": user.id})
