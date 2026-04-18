from django.forms import ModelForm, Textarea
from .models import (User, Todo, Image)
from django import forms

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ["titulo","anotacao","prioridade","tag","prazo_inicial", "prazo_final", "completo", "favorito"]
        widgets = {
            "anotacao": Textarea(attrs={"cols": 80, "rows": 20}),

            'prazo_final': forms.DateInput(
                attrs={
                    'type': 'date', # Isso usará o widget de data nativo do navegador
                    'class': 'form-control', # Exemplo de classe CSS (Bootstrap)
                    # 'placeholder': 'AAAA-MM-DD' # Se não usar type='date'
                },
                format='%Y-%m-%d' # Formato que o widget espera/envia (ISO 8601 é bom para type='date')
            ),

            'prazo_inicial': forms.DateInput(
                attrs={
                    'type': 'date', # Isso usará o widget de data nativo do navegador
                    'class': 'form-control', # Exemplo de classe CSS (Bootstrap)
                    # 'placeholder': 'AAAA-MM-DD' # Se não usar type='date'
                },
                format='%Y-%m-%d' # Formato que o widget espera/envia (ISO 8601 é bom para type='date')
            ),
        }

        labels = {
            "anotacao": "Anotação",
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(
        label="Senha:",
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "Digite sua senha"
            }
        )
    )

    class Meta:
        model = User
        fields = ["username", "password"]
        labels = {
            "username": "Nome:",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "Digite seu nome de usuário"
                }
            ),
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        # Inclua os campos do seu modelo Image que o usuário deve preencher
        fields = ['titulo', 'observacao', 'img']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Título da imagem'}),
            'observacao': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Alguma observação sobre a imagem...', 'rows': 3}),
            'img': forms.ClearableFileInput(attrs={'class': 'file-input'}),
        }
