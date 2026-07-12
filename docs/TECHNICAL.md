**ToDo — Documentação Técnica (resumo)**

Estrutura principal (src/)
- `core`: configurações do Django, middleware e inicialização.
- `main`: modelos e views centrais (ver `docs/apps/main.md`).
- `agenda`: calendário (ver `docs/apps/agenda.md`).
- `checklist`: checklists (ver `docs/apps/checklist.md`).

Pontos técnicos importantes
- Settings carrega `.envs/.env` (veja `src/core/settings.py`). Certifique-se de manter `SECRET_KEY` seguro.
- Autorização: regras encapsuladas nos models (`pode_editar`, `pode_excluir`, manager `para_usuario`). Ao retomar, concentre mudanças nestes pontos se precisar alterar permissão.
- Banco: SQLite por padrão. Para produção, recomenda-se migrar para PostgreSQL.

Como localizar código frequentemente editado
- Templates: `src/*/templates/`.
- URLs: `src/*/urls.py` (ver `src/core/urls.py` para rotas globais).
- Forms: `src/*/forms.py`.

Testes e ambiente de desenvolvimento
- Não foram encontrados testes automatizados específicos deste app além de exemplos em outros projetos. Recomendo adicionar testes básicos (smoke tests) antes de mudanças significativas.

Limpeza aplicada
- Remoção de prints de debug em `agenda/classes.py` e `core/settings.py`.
