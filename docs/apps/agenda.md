**App `agenda`**

Responsabilidade
- Calendário e eventos por usuário. Suporte a cores por usuário e CRUD de eventos.

Principais modelos e formulários
- `AgendaModel`: representa um evento com campos de data/horário e `is_active`.
- `Colors`: cor de destaque por usuário.
- `AgendaForm`, `ColorForm` — formulários usados para criar/editar eventos e cores.

Principais fluxos
- `agenda`: exibe o mês corrente, reúne eventos com `eventos_por_dia` para renderizar o calendário.
- `eventos_`, `detalhe_sobre_evento`: listagem e detalhe do evento.
- `configs`, `delete_event`, `edit_event`: editar preferências e eventos.

Observações
- Removidos prints de debug para evitar poluição de logs. Form.errors é tratado pelo fluxo de formulário nas templates.
