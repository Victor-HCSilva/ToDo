from django.shortcuts import render, redirect
from django.http import HttpResponse
from checklist.models import Titulo, Itens
from checklist.forms import ItensForm, TituloForm


def checklist(request):
    titulo_form = TituloForm()
    itens_form = ItensForm()

    if request.method == "POST":
        if "submit_titulo" in request.POST:
            titulo_form = TituloForm(request.POST)
            if titulo_form.is_valid():
                titulo = titulo_form.save(commit=False)
                titulo.user = request.user
                titulo.save()
                return redirect("anotacoes")

        elif "submit_itens" in request.POST:
            itens_form = ItensForm(request.POST)
            if itens_form.is_valid():
                item = itens_form.save(commit=False)
                item.user = request.user
                item.save()
                return redirect("anotacoes")

    titulos = Titulo.objects.filter(user=request.user)
    itens = Itens.objects.filter(user=request.user)

    return render(
        request,
        "checklist.html",
        {
            "titulo_form": titulo_form,
            "itens_form": itens_form,
            "titulos": titulos,
            "itens": itens,
        },
    )
