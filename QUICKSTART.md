# 🚀 Começar Aqui - Sistema de Colaboração

Este é o seu guia rápido para ativar o sistema de colaboração no projeto ToDo.

---

## ⚡ 5 Minutos de Setup

### 1. Aplicar Migrações

```bash
cd /home/victor/main/to-do/ToDo
python src/manage.py makemigrations main
python src/manage.py migrate
```

### 2. Testar no Shell

```bash
python src/manage.py shell

# Criar grupo
from main.models import CollaborationGroup
from django.contrib.auth.models import User

user = User.objects.get(username='your_username')
grupo = CollaborationGroup.objects.create(
    name="Meu Primeiro Grupo",
    descricao="Grupo de teste",
    owner=user
)

# Adicionar membro
outro_user = User.objects.get(username='outro_usuario')
grupo.adicionar_membro(outro_user)

print(f"Grupo criado: {grupo.name}")
print(f"Membros: {grupo.membros.all()}")
```

### 3. Acessar na Web

1. Abra http://localhost:8000/grupos/
2. Clique "Novo Grupo"
3. Preencha o formulário
4. Pronto!

---

## 📋 Checklist Antes de Usar

- [ ] Migrações aplicadas sem erros
- [ ] Templates criados em `src/main/templates/grupos/`
  - [ ] `listar_grupos.html`
  - [ ] `grupo_form.html`
  - [ ] `deletar_grupo.html`
  - [ ] `gerenciar_membros.html`
- [ ] Pode acessar `/grupos/` sem erro 404
- [ ] Pode criar grupo
- [ ] Pode adicionar membros
- [ ] Pode compartilhar Todo com grupo

---

## 🎯 Casos de Uso Imediatos

### 1. Projeto em Equipe
```
1. Criar grupo "Team X"
2. Adicionar membros do time
3. Compartilhar pasta do projeto com o grupo
4. Todos veem todos os Todos do projeto
```

### 2. Colaboração Ad-Hoc
```
1. Todo que precisa ser revisado
2. Adicionar colega direto como collaborador
3. Colega edita o Todo
4. Pronto!
```

### 3. Múltiplos Projetos
```
1. Projeto A: Compartilhado com "Time Backend"
2. Projeto B: Compartilhado com "Time Frontend"
3. Projeto C: Compartilhado com ambos os times
```

---

## 📁 Arquivos Modificados

```
✅ models.py         → Novo: CollaborationGroup
✅ forms.py          → Novos forms com suporte a grupos
✅ views.py          → 5 novas views
✅ urls.py           → 5 novas rotas
✅ templates/grupos/ → 4 novos templates (criados)
```

---

## 🔍 Estrutura de Permissões

```
ACESSO = (
    Usuário é dono 
    OU colaborador direto
    OU membro de grupo com acesso
    OU está em pasta compartilhada
    OU em grupo de pasta compartilhada
)
```

---

## 💡 Dicas

- **Passe o tempo**: O QuerySet `.distinct()` evita duplicatas ao usar múltiplos critérios
- **Segurança**: Sempre verificar `pode_editar()` antes de renderizar
- **Performance**: Usar `.prefetch_related('membros')` em listas grandes
- **UX**: Adicionar ícones visuais para indicar "compartilhado com grupo"

---

## 🆘 Se Algo Quebrar

```bash
# Reset do banco (cuidado!)
python src/manage.py migrate main zero
python src/manage.py migrate main

# Limpar cache
python src/manage.py clear_cache

# Verificar status
python src/manage.py showmigrations main
```

---

## 📚 Documentação Completa

- [COLLABORATION_ARCHITECTURE.md](COLLABORATION_ARCHITECTURE.md) - Arquitetura técnica
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - O que foi implementado
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Guia de testes

---

## ✨ Próximos Passos (Opcional)

Após validar tudo:
- [ ] Adicionar níveis de permissão (read/write/admin)
- [ ] Sistema de notificações
- [ ] Histórico de quem editou o quê
- [ ] Compartilhamento com expiração
- [ ] Convites em lugar de adição direta

---

## 🎓 Exemplos de Código

### Criar grupo com membros
```python
grupo = CollaborationGroup.objects.create(
    name="Team Backend",
    owner=request.user
)
grupo.membros.set([user1, user2, user3])
```

### Compartilhar Todo com grupo
```python
todo = Todo.objects.get(id=1)
grupo = CollaborationGroup.objects.get(id=1)
todo.grupos_colaboracao.add(grupo)
```

### Ver todos acessíveis ao usuário
```python
meus_todos = Todo.objects.para_usuario(request.user)
```

### Verificar permissão
```python
if todo.pode_editar(request.user):
    # Permitir edição
else:
    return HttpResponseForbidden()
```

---

## 🎉 Parabéns!

Você agora tem um sistema completo de colaboração. Aproveite!

**Qualquer dúvida**, consulte a documentação ou execute os testes.

---

*Implementado em: 11 de julho de 2026*
*Versão: 1.0*
