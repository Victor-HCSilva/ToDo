**App `main`**

Responsabilidade
- Gerencia as anotações/tarefas (model `Todo`), pastas (`Folder`), imagens (`Image`) e grupos de colaboração (`CollaborationGroup`).

Principais modelos
- `Todo`: campo `user`, `titulo`, `anotacao`, `prazo_inicial`/`prazo_final`, `is_active` e relacionamentos com `Folder`, colaboradores e `CollaborationGroup`.
- `Folder`: organização de `Todo` por usuário, com compartilhamento por `colaboradores` e `grupos_colaboracao`.
- `CollaborationGroup`: grupos de usuários para compartilhar itens.

Principais views (function-based)
- `anotacoes`: lista de anotações visíveis para o usuário (usa manager `para_usuario`).
- `show`, `editar`, `remover`: CRUD básico de `Todo` com checagens de permissão (`pode_editar`, `pode_excluir`).
- `create_todo`, `folder_list_create`, `folder_update`, `folder_delete`: criação e gerenciamento de pastas e tarefas.

Observações
- Lógica de autorização está principalmente nos models (`pode_editar`, manager `para_usuario`) — bom para manter regras centralizadas.
- Use os forms em `main/forms.py` para validar inputs no frontend.
