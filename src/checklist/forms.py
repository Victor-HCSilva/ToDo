from django import forms

from checklist.models import Item, Link, Tarefa


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "descricao",
            "feito",
            "color",
            "tarefa",  # permite escolher a qual título o item pertence
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["titulo"].queryset = Tarefa.objects.filter(user=user)


class TituloForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ["titulo", "color", "todo"]


class LinkForm(forms.ModelForm):
    """Contexto de tarefa deve ser adicionada no momento de salvar"""

    class Meta:
        model = Link
        fields = ["url"]
