from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def prioridade(request, id_user):
    if request.user.id != id_user:
        return redirect("login")

    return render(request, "prioridade.html")
