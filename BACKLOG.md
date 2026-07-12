BACKLOG

Interface
- Ajustar contrastes e responsividade dos cards (UX).
- Corrigir ícones quebrados em alguns templates.

UX
- Melhorar fluxo de adição de colaboradores com autocomplete.
- Adicionar confirmação modal antes de soft-delete global.

Backend
- Adicionar testes unitários para `main.models` e views importantes.
- Implementar validação mais forte nos forms (server-side).

Arquitetura
- Considerar extração de API (DRF) quando houver necessidade de clients externos.

Performance
- Otimizar consultas N+1 (revisar `select_related` e `prefetch_related`).

Segurança
- Garantir valores seguros em `.env` e rotinas de backup para `SECRET_KEY`.
- Revisar configurações de `ALLOWED_HOSTS` e `CORS`.

Testes
- Adicionar testes de integração para rota de criação/edição de `Todo`.

Melhorias gerais
- Remover código legado em `init` quando for seguro.
- Padronizar mensagens e traduções (i18n) se necessário.
