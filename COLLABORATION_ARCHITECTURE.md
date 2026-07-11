# Arquitetura de Colaboração - ToDo App

## Visão Geral

O sistema de colaboração do ToDo App permite que usuários compartilhem anotações (Todos) e pastas com outros usuários através de:

1. **Colaboradores Individuais** - Compartilhamento direto com usuários específicos
2. **Grupos de Colaboração** - Compartilhamento com múltiplos usuários organizados em grupos

---

## Modelos de Dados

### 1. `CollaborationGroup`
Define um grupo de colaboradores que pode ser reutilizado para compartilhar múltiplos itens.

```python
class CollaborationGroup(models.Model):
    name: CharField              # Nome único do grupo por owner
    descricao: TextField         # Descrição do propósito do grupo
    owner: ForeignKey(User)      # Criador e proprietário do grupo
    membros: ManyToMany(User)    # Usuários que pertencem ao grupo
    created_at: DateTimeField
    updated_at: DateTimeField
    is_active: BooleanField      # Para exclusão lógica
```

**Métodos principais:**
- `adicionar_membro(user)` - Adiciona usuário ao grupo
- `remover_membro(user)` - Remove usuário do grupo
- `pode_gerenciar(user)` - Verifica se usuário pode gerenciar o grupo

---

### 2. `Folder` (Pasta)
Estrutura básica para organizar Todos. Agora suporta colaboradores individuais e grupos.

```python
class Folder(models.Model):
    name: CharField
    user: ForeignKey(User)                    # Proprietário
    colaboradores: ManyToMany(User)           # Colaboradores individuais
    grupos_colaboracao: ManyToMany(CollaborationGroup)  # Grupos
    is_active: BooleanField
```

**Novos métodos:**
- `pode_editar(user)` - Verifica se usuário pode editar a pasta
- `pode_excluir(user)` - Verifica se usuário pode deletar a pasta

---

### 3. `Todo` (Anotação)
Itens de tarefas/anotações com suporte completo a colaboração.

```python
class Todo(models.Model):
    user: ForeignKey(User)                    # Proprietário
    titulo: CharField
    anotacao: TextField
    folder: ForeignKey(Folder, null=True)    # Pode estar em uma pasta ou solto
    colaboradores: ManyToMany(User)           # Colaboradores individuais
    grupos_colaboracao: ManyToMany(CollaborationGroup)  # Grupos
    # ... outros campos
```

**Novos métodos:**
- `pode_editar(user)` - Verifica se usuário pode editar
- `pode_excluir(user)` - Verifica se usuário pode deletar (apenas owner)

---

## Lógica de Permissões

### Hierarquia de Acesso para Todos

Um usuário **pode visualizar e editar** um Todo se:

1. ✅ É o proprietário (`user == request.user`)
2. ✅ É um colaborador direto (`colaboradores.filter(id=user.id)`)
3. ✅ Pertence a um grupo com acesso (`grupos_colaboracao.filter(membros=user)`)
4. ✅ É colaborador da pasta pai (`folder.colaboradores.filter(id=user.id)`)
5. ✅ Pertence a um grupo da pasta pai (`folder.grupos_colaboracao.filter(membros=user)`)
6. ✅ É proprietário da pasta pai (`folder.user == user`)

```python
# Implementação no QuerySet
class TodoQuerySet(models.QuerySet):
    def para_usuario(self, user):
        user_groups = CollaborationGroup.objects.filter(membros=user)
        
        return self.filter(
            Q(user=user)                                    # 1. Proprietário
            | Q(colaboradores=user)                         # 2. Colaborador direto
            | Q(grupos_colaboracao=user_groups)             # 3. Membro de grupo
            | Q(folder__colaboradores=user)                 # 4. Colaborador da pasta
            | Q(folder__grupos_colaboracao=user_groups)     # 5. Grupo da pasta
            | Q(folder__user=user)                          # 6. Proprietário da pasta
        ).distinct()
```

### Permissões de Edição e Exclusão

```python
# Editar
- Proprietário do Todo
- Colaborador direto do Todo
- Membro de grupo com acesso ao Todo
- Qualquer pessoa com permissão na pasta pai

# Excluir
- Apenas o proprietário do Todo
- OU o proprietário da pasta pai
```

---

## Views de Colaboração

### Gerenciar Colaboradores Individuais

```
POST /colaboradores/<tipo>/<pk>/
    tipo: 'todo' ou 'folder'
    pk: id do objeto
    
    Ações:
    - add_user: Adiciona colaborador por username
    - remove_user: Remove colaborador existente
```

### Gerenciar Grupos

```
GET  /grupos/                           # Listar todos os grupos do usuário
GET  /grupos/criar/                     # Formulário de criação
POST /grupos/criar/                     # Criar novo grupo
GET  /grupos/<id>/editar/               # Formulário de edição
POST /grupos/<id>/editar/               # Atualizar grupo
GET  /grupos/<id>/deletar/              # Confirmação de exclusão
POST /grupos/<id>/deletar/              # Deletar grupo
GET  /grupos/<id>/membros/              # Gerenciar membros
POST /grupos/<id>/membros/              # Adicionar/remover membros
```

---

## Forms de Colaboração

### `TodoFormComColaboradores`
Form estendido para criar/editar Todos com opção de adicionar colaboradores.

```python
fields = [
    "titulo",
    "anotacao",
    "folder",
    "colaboradores",           # Novo
    "grupos_colaboracao",      # Novo
    # ... outros campos
]
```

### `FolderFormComColaboradores`
Form para gerenciar acesso em pastas.

```python
fields = [
    "name",
    "colaboradores",           # Novo
    "grupos_colaboracao",      # Novo
]
```

### `CollaborationGroupForm`
Form para criar e editar grupos.

```python
fields = [
    "name",
    "descricao",
    "membros"
]
```

---

## Fluxo de Compartilhamento

### 1️⃣ Compartilhar Todo com Colaborador Individual

```
1. Ir para view de show do Todo
2. Clicar em "Gerenciar Colaboradores"
3. Digitar username do colaborador
4. Clicar "Adicionar"
5. Colaborador agora pode editar o Todo
```

### 2️⃣ Criar Grupo e Compartilhar

```
1. Ir para /grupos/
2. Clicar "Criar Novo Grupo"
3. Preencher nome e descrição
4. Adicionar membros
5. Usar grupo ao compartilhar Todos/Pastas
```

### 3️⃣ Compartilhar Pasta com Grupo

```
1. Ir para /folders/
2. Selecionar pasta
3. Clicar "Editar"
4. Adicionar grupo no campo "grupos_colaboracao"
5. Salvar
6. Todos os membros do grupo têm acesso aos Todos da pasta
```

---

## Casos de Uso

### Caso 1: Projeto em Equipe
- **Cenário**: Time de projeto com 5 pessoas
- **Solução**: Criar grupo "Time Projeto X" com todos os membros
- **Resultado**: Compartilhar pasta principal com o grupo; todos veem todos os Todos

### Caso 2: Revisão por Colega
- **Cenário**: Quero que João revise uma anotação específica
- **Solução**: Ir ao Todo, adicionar João como colaborador direto
- **Resultado**: João pode ver e editar apenas esse Todo

### Caso 3: Múltiplos Grupos
- **Cenário**: Trabalho em 3 projetos diferentes com times diferentes
- **Solução**: Criar 3 grupos diferentes; compartilhar pastas com seus respectivos grupos
- **Resultado**: Cada grupo acessa apenas seu projeto

---

## Segurança e Validações

### Validações Implementadas

1. ✅ Apenas proprietário pode gerenciar grupo
2. ✅ Usuário não pode ser proprietário e colaborador simultaneamente
3. ✅ Apenas proprietário ou dono da pasta pode deletar
4. ✅ QuerySet garante visibilidade apenas de itens acessíveis
5. ✅ Views verificam permissões antes de renderizar/editar
6. ✅ Exclusão lógica com `is_active` para auditoria

### Melhorias Sugeridas

- [ ] Adicionar níveis de permissão (view-only, edit, admin)
- [ ] Implementar logs de atividades de colaboração
- [ ] Notificações quando adicionado a grupo/compartilhado
- [ ] Limite de membros por grupo (opcional)
- [ ] Convites em vez de adição direta
- [ ] Revogar acesso por tempo (compartilhamento temporal)

---

## Operações do Admin

### Criar grupo via Python shell

```python
from main.models import CollaborationGroup
from django.contrib.auth.models import User

user = User.objects.get(username='victor')
grupo = CollaborationGroup.objects.create(
    name="Time Backend",
    descricao="Grupo do time backend",
    owner=user
)

# Adicionar membros
membro1 = User.objects.get(username='alice')
grupo.adicionar_membro(membro1)
```

### Compartilhar Todo com grupo

```python
from main.models import Todo, CollaborationGroup

todo = Todo.objects.get(id=1)
grupo = CollaborationGroup.objects.get(id=1)
todo.grupos_colaboracao.add(grupo)
```

---

## Migrações Necessárias

```bash
# Gerar migrações
python manage.py makemigrations main

# Aplicar migrações
python manage.py migrate
```

### Alterações do banco de dados:
- Novo modelo: `CollaborationGroup`
- Nova tabela: `main_todo_grupos_colaboracao` (M2M)
- Nova tabela: `main_folder_grupos_colaboracao` (M2M)
- Nova tabela: `main_collaborationgroup_membros` (M2M)

---

## Templates Necessários

Criar os seguintes templates em `src/main/templates/grupos/`:

1. `listar_grupos.html` - Lista todos os grupos
2. `grupo_form.html` - Formulário de criar/editar
3. `deletar_grupo.html` - Confirmação de exclusão
4. `gerenciar_membros.html` - Adicionar/remover membros

---

## Resumo de Arquivos Modificados

| Arquivo | Mudanças |
|---------|----------|
| `models.py` | Novo: `CollaborationGroup`; Atualizado: `Folder`, `Todo` com grupos |
| `forms.py` | Novos: `TodoFormComColaboradores`, `FolderFormComColaboradores`, `CollaborationGroupForm`, `AddColaboradorForm` |
| `views.py` | Novos: 5 views para gerenciar grupos |
| `urls.py` | Novos: 5 rotas para grupos |

---

## Próximos Passos

1. ✅ Executar migrações
2. ⭕ Criar templates de gerenciamento de grupos
3. ⭕ Atualizar templates existentes para mostrar botão de colaboradores
4. ⭕ Testar fluxo completo de colaboração
5. ⭕ Considerar melhorias sugeridas acima

---

**Versão**: 1.0  
**Data**: 2026-07-11  
**Autor**: GitHub Copilot
