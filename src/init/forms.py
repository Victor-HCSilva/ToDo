# from django import forms
# from django.forms import ModelForm, Textarea

# from .models import Folder, Image, Todo, User


# class TodoForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         # Removemos o argumento 'user' do kwargs para não dar erro no super()
#         user = kwargs.pop("user", None)
#         super().__init__(*args, **kwargs)

#         # Se o usuário foi passado, filtramos as opções dos campos desejados
#         if user:
#             self.fields["folder"].queryset = Folder.objects.filter(user=user)

#             # Se o campo 'tag' também for associado ao usuário, você pode filtrar da mesma forma:
#             # self.fields['tag'].queryset = Tag.objects.filter(user=user)

#     class Meta:
#         model = Todo
#         fields = [
#             "titulo",
#             "anotacao",
#             "prioridade",
#             "tag",
#             "prazo_inicial",
#             "prazo_final",
#             "completo",
#             "favorito",
#             "folder",
#         ]

#         widgets = {
#             # Adicionamos a classe 'textarea' do Bulma aqui
#             "anotacao": Textarea(
#                 attrs={
#                     "class": "textarea",
#                     "rows": 20,
#                     "placeholder": "Escreva sua anotação aqui...",
#                 }
#             ),
#             # Adicionamos a classe 'input' do Bulma para os campos de data
#             "prazo_final": forms.DateInput(
#                 attrs={"type": "date", "class": "input"}, format="%Y-%m-%d"
#             ),
#             "prazo_inicial": forms.DateInput(
#                 attrs={"type": "date", "class": "input"}, format="%Y-%m-%d"
#             ),
#         }
#         labels = {
#             "anotacao": "Anotação",
#         }


# class UserForm(forms.ModelForm):
#     password = forms.CharField(
#         label="Senha:",
#         widget=forms.PasswordInput(
#             attrs={"class": "input", "placeholder": "Digite sua senha"}
#         ),
#     )

#     class Meta:
#         model = User
#         fields = ["username", "password"]
#         labels = {
#             "username": "Nome:",
#         }
#         widgets = {
#             "username": forms.TextInput(
#                 attrs={"class": "input", "placeholder": "Digite seu nome de usuário"}
#             ),
#         }


# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         # Inclua os campos do seu modelo Image que o usuário deve preencher
#         fields = ["titulo", "observacao", "img"]
#         widgets = {
#             "titulo": forms.TextInput(
#                 attrs={"class": "input", "placeholder": "Título da imagem"}
#             ),
#             "observacao": forms.Textarea(
#                 attrs={
#                     "class": "textarea",
#                     "placeholder": "Alguma observação sobre a imagem...",
#                     "rows": 3,
#                 }
#             ),
#             "img": forms.ClearableFileInput(attrs={"class": "file-input"}),
#         }


# class FolderForm(forms.ModelForm):
#     class Meta:
#         model = Folder
#         fields = ["name"]
