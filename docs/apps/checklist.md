**App `checklist`**

Responsabilidade
- Gerencia checklists com `Tarefa`, `Item` e `Link`.

Principais modelos
- `Tarefa`: título, cor, usuário e `is_active`.
- `Item`: descrição, status (`nao_iniciado`, `fazendo`, `concluido`, `cancelado`), cor, referência à `Tarefa`.
- `Link`: URL vinculada à `Tarefa`.

Principais fluxos
- `checklist` view: múltiplas ações via POST (criar tarefa, adicionar item/link, editar, soft-delete). Usa `Prefetch` para otimizar carregamento de itens/links.

Observações
- As ações rápidas estão centralizadas numa view; para manutenção futura, considere separar handlers por responsabilidade (fora do escopo do freeze).
