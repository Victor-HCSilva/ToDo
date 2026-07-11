# Guia de Testes e Validação - Sistema de Colaboração

## 🚀 Começando

### 1. Gerar e Aplicar Migrações

```bash
cd /home/victor/main/to-do/ToDo

# Gerar migrações
python src/manage.py makemigrations main

# Aplicar migrações
python src/manage.py migrate
```

**Esperado**: Sem erros. Novas tabelas criadas no banco de dados.

---

## ✅ Testes Básicos

### Teste 1: Criar um Grupo

**Objetivo**: Verificar se é possível criar grupos de colaboração

**Passos**:
1. Fazer login no sistema
2. Ir para `/grupos/`
3. Clicar "Novo Grupo"
4. Preencher:
   - Nome: "Time Backend"
   - Descrição: "Grupo do time de desenvolvimento backend"
   - Adicionar 2-3 membros
5. Salvar

**Esperado**: 
- ✅ Grupo criado com sucesso
- ✅ Redirecionado para lista de grupos
- ✅ Grupo aparece na lista com membros corretos

---

### Teste 2: Editar Grupo

**Objetivo**: Verificar se é possível editar grupos

**Passos**:
1. Na lista de grupos, clicar em "Editar" (ícone de lápis)
2. Mudar o nome para "Time DevOps"
3. Adicionar mais um membro
4. Salvar

**Esperado**:
- ✅ Grupo atualizado com sucesso
- ✅ Novo nome aparece na lista
- ✅ Novo membro adicionado

---

### Teste 3: Gerenciar Membros

**Objetivo**: Verificar adição e remoção de membros

**Passos**:
1. Na lista de grupos, clicar "Membros"
2. Adicionar novo usuário por username
3. Verificar se aparece na tabela
4. Remover um membro
5. Verificar se desaparece da tabela

**Esperado**:
- ✅ Novos membros aparecem imediatamente
- ✅ Membros removidos desaparecem
- ✅ Mensagens de sucesso aparecem

---

### Teste 4: Compartilhar Todo com Grupo

**Objetivo**: Verificar se Todos podem ser compartilhados com grupos

**Pré-requisitos**:
- Usuário 1 (dono) logado
- Grupo criado com Usuário 2 como membro
- Todo criado por Usuário 1

**Passos**:
1. Ir para o Todo
2. Clicar "Editar"
3. Encontrar campo "Grupos de Colaboração"
4. Selecionar o grupo criado
5. Salvar

**Esperado**:
- ✅ Campo de grupos aparece no form
- ✅ Grupo pode ser selecionado
- ✅ Todo é salvo com o grupo

---

### Teste 5: Verificar Visibilidade (Crítico!)

**Objetivo**: Garantir que permissões funcionam corretamente

**Pré-requisitos**:
- Usuário 1 (criou o Todo)
- Usuário 2 (membro do grupo)
- Todo compartilhado com grupo
- Usuário 3 (não no grupo)

**Passos**:
1. **Usuário 1** vai para `/anotacoes/1`
   - ✅ Deve ver o Todo
2. **Usuário 2** (membro do grupo) vai para `/anotacoes/2`
   - ✅ Deve ver o Todo no QuerySet
3. **Usuário 3** vai para `/anotacoes/3`
   - ✅ NÃO deve ver o Todo

**Validações de Segurança**:
- Usuário 2 tenta editar: ✅ Deve funcionar
- Usuário 3 tenta editar: ✅ Deve receber HttpResponseForbidden

---

### Teste 6: Compartilhar Pasta com Grupo

**Objetivo**: Verificar acesso de Todos através de pasta compartilhada

**Pré-requisitos**:
- Usuário 1 dono de Pasta
- Grupo com Usuário 2 como membro
- Todos dentro da Pasta

**Passos**:
1. Ir para `/folders/`
2. Selecionar pasta
3. Clicar "Editar"
4. Adicionar grupo em "Grupos de Colaboração"
5. Salvar

**Esperado**:
- ✅ Usuário 1 continua vendo todos os Todos
- ✅ Usuário 2 vê todos os Todos da pasta
- ✅ Usuário 3 (não no grupo) não vê

---

### Teste 7: Hierarquia de Permissões

**Objetivo**: Verificar que a hierarquia de permissões funciona corretamente

**Casos**:

**Caso A: Todo em Pasta Compartilhada**
```
Usuário 1: Dono do Todo ✅ Pode editar
Usuário 2: Collaborador da Pasta ✅ Pode editar (via pasta)
Usuário 3: Nenhuma relação ❌ Não pode editar
```

**Caso B: Todo com Collaborador Individual E Grupo**
```
Usuário 1: Dono ✅ Pode editar
Usuário 2: Collaborador individual ✅ Pode editar
Usuário 3: Membro de grupo ✅ Pode editar
Usuário 4: Nenhuma relação ❌ Não pode editar
```

**Caso C: Remover de Grupo**
```
1. Usuário 2 é membro do grupo
2. Usuário 2 vê Todo compartilhado com grupo
3. Remover Usuário 2 do grupo
4. Usuário 2 AGORA NÃO pode mais ver o Todo
```

---

## 🔍 Testes Avançados

### Teste 8: Performance com Muitos Grupos

**Objetivo**: Verificar performance do QuerySet

**Setup**:
```python
# Executar no Django shell
from main.models import CollaborationGroup, Todo
from django.contrib.auth.models import User

user = User.objects.first()

# Criar 50 grupos
for i in range(50):
    group = CollaborationGroup.objects.create(
        name=f"Grupo {i}",
        owner=user
    )
    group.membros.add(User.objects.all()[:5])

# Medir tempo
import time
start = time.time()
todos = Todo.objects.para_usuario(user)
end = time.time()
print(f"Tempo: {end - start:.2f}s")
```

**Esperado**:
- ✅ Tempo < 1 segundo
- ✅ QuerySet usa `.distinct()` para evitar duplicatas

---

### Teste 9: Exclusão Lógica

**Objetivo**: Verificar que grupos deletados não aparecem mais

**Passos**:
1. Notar ID do grupo (ex: 5)
2. Deletar grupo via interface
3. Ir para `/grupos/`
4. Grupo NÃO deve aparecer
5. Verificar banco: `is_active=False`

**Esperado**:
- ✅ Grupo não aparece na lista
- ✅ Campo `is_active` muda para False
- ✅ Não é exclusão física (auditoria)

---

### Teste 10: Validações de Segurança

**Objetivo**: Garantir que validações funcionam

**Teste 10a: Não pode ser dono e collaborador**
```python
grupo.adicionar_membro(grupo.owner)
# Esperado: Funcionará mas semanticamente errado
# Melhoria: Adicionar validação no form
```

**Teste 10b: Apenas owner pode deletar grupo**
```
1. Usuário 1: Criador do grupo
2. Usuário 2: Membro do grupo
3. Usuário 2 tenta acessar /grupos/1/deletar/
# Esperado: ❌ 404 ou Forbidden
```

**Teste 10c: Usuário não pode ver grupos de outros**
```
1. Usuário 1 acessa /grupos/2/editar/ (grupo de User 2)
# Esperado: ❌ 404
```

---

## 🐛 Checklist de Debug

Se algo não funcionar, verificar:

- [ ] Migrações foram aplicadas? `python manage.py migrate`
- [ ] Novas tabelas existem no banco? `python manage.py dbshell`
- [ ] Usuários existem? `User.objects.count()`
- [ ] QuerySet está usando `.distinct()`? Verificar em `models.py`
- [ ] Templates foram criados em `grupos/`?
- [ ] URLs foram adicionadas em `urls.py`?
- [ ] Forms estão importando `CollaborationGroup`?
- [ ] Views estão registradas em `views.py`?

---

## 📊 Relatório de Teste

Preencha após rodar os testes:

```
Teste 1 (Criar Grupo):           [ ] PASSOU [ ] FALHOU
Teste 2 (Editar Grupo):          [ ] PASSOU [ ] FALHOU
Teste 3 (Gerenciar Membros):     [ ] PASSOU [ ] FALHOU
Teste 4 (Compartilhar Todo):     [ ] PASSOU [ ] FALHOU
Teste 5 (Visibilidade):          [ ] PASSOU [ ] FALHOU
Teste 6 (Compartilhar Pasta):    [ ] PASSOU [ ] FALHOU
Teste 7 (Hierarquia):            [ ] PASSOU [ ] FALHOU
Teste 8 (Performance):           [ ] PASSOU [ ] FALHOU
Teste 9 (Exclusão Lógica):       [ ] PASSOU [ ] FALHOU
Teste 10 (Validações):           [ ] PASSOU [ ] FALHOU
```

---

## 🚨 Problemas Conhecidos

### Problema 1: Campo "Grupos de Colaboração" não aparece em TodoForm
**Causa**: TodoForm básico não inclui o campo
**Solução**: Usar `TodoFormComColaboradores` nas views

### Problema 2: QuerySet lento com muitos grupos
**Causa**: Sem índices no banco
**Solução**: Adicionar índices nas migrations futuras

### Problema 3: Usuário não vê changes depois de adicionar a grupo
**Causa**: Página em cache
**Solução**: F5 para limpar cache

---

## 📚 Recursos

- [COLLABORATION_ARCHITECTURE.md](COLLABORATION_ARCHITECTURE.md) - Documentação técnica completa
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Resumo de mudanças
- Django QuerySet docs: https://docs.djangoproject.com/en/stable/ref/models/querysets/

---

## ✨ Próximas Melhorias Sugeridas

Após validar os testes:

- [ ] Adicionar níveis de permissão (view-only, edit, admin)
- [ ] Sistema de convites (em vez de adição direta)
- [ ] Notificações de colaboração
- [ ] Logs de atividade
- [ ] Compartilhamento com expiração
- [ ] Interface visual de permissões (ACL)
- [ ] Histórico de alterações

---

**Data**: 11 de julho de 2026
**Status**: Pronto para testes
