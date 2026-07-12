**ToDo — Arquitetura (resumo)**

- Tipo: Monólito Django (apps organizados por domínio funcional).
- Linguagem: Python 3.12; Framework: Django 5.x.
- Banco de dados: SQLite por padrão (arquivo `src/db.sqlite3`).
- Local das views e templates: templates em `src/*/templates`, rotas em `src/*/urls.py`.

Apps principais
- `main`: Gerencia os modelos centrais (Todo, Folder, Image, CollaborationGroup) e as views de CRUD, autenticação mínima e home.
- `agenda`: Fornece calendário e eventos (modelo `AgendaModel`, cores por usuário).
- `checklist`: Lista de tarefas com itens e links (Tarefa, Item, Link).

Decisões arquiteturais importantes (porquê)
- Monólito: facilita desenvolvimento e deploy para um projeto pequeno; evita overhead de APIs e separação.
- Não usar DRF: não há necessidade de API REST pública no escopo atual.
- SQLite por padrão: simplicidade para desenvolvedores e testes rápidos; troque por Postgres em produção quando necessário.

Pontos de atenção
- Há código legado e blocos comentados em `src/init/` (mantidos intencionalmente)
- Variáveis de ambiente carregadas de `.envs/.env` (veja `src/core/settings.py`) — garanta backup seguro.
- Pequenas mensagens de debug removidas do `settings.py` e `agenda/classes.py` para evitar log poluído.

Como retomar o desenvolvimento (checklist rápido)
1. Ativar `.venv` e instalar dependências.
2. Criar superuser (`python src/manage.py createsuperuser`).
3. Rodar migrações (`python src/manage.py migrate`).
4. Rodar servidor local (`python src/manage.py runserver`).
