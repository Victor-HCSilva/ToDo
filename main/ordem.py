from django.shortcuts import render
from init.models import Todo, User
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from init.forms import TodoForm


@login_required
def prioridade(request, id_user):
    if request.user.id != id_user:
        return redirect("login")

    return render(request, "prioridade.html")
