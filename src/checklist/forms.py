from django import forms
from checklist.models import Titulo, Itens


class ItensForm(forms.ModelForm):
    class Meta:
        model = Itens
        fields = [
            "label",
            "feito",
            "color",
            "titulo",  # permite escolher a qual título o item pertence
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["titulo"].queryset = Titulo.objects.filter(user=user)


class TituloForm(forms.ModelForm):
    class Meta:
        model = Titulo
        fields = [
            "titulo",
            "color",
        ]
