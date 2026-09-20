Você vai trabalhar no projeto ToDo existente neste repositório:

https://github.com/Victor-HCSilva/ToDo

Quero que você faça a separação da camada de API do projeto atual, preparando o backend Django para deixar de depender diretamente dos templates HTML.

Objetivo

Transformar o Django atual em um backend que exponha uma API HTTP, preferencialmente REST/JSON  (use DRF para tal) , mantendo as funcionalidades e regras de negócio existentes.

A interface atual pode continuar existindo temporariamente durante a migração. Não quero que você reescreva o frontend inteiro agora.

A prioridade desta etapa é construir uma API funcional e bem estruturada que posteriormente possa ser consumida tanto por:

HTML/CSS/JavaScript puro;
Next.js/React;
eventualmente outros clientes.

A arquitetura final desejada é:

Cliente
↓
Django API
↓
Models / regras de negócio
↓
Banco de dados

1. Primeiro analise o projeto

Antes de modificar qualquer código:

Analise a estrutura completa do projeto.
Identifique os apps Django existentes.
Identifique todos os models.
Identifique as relações entre os models.
Identifique as views existentes.
Identifique os forms.
Identifique as regras de autorização/permissão.
Identifique uploads de arquivos/imagens.
Identifique autenticação e gerenciamento de sessão.
Identifique todas as URLs existentes.
Identifique quais funcionalidades dependem diretamente de templates Django.
Identifique possíveis dependências entre funcionalidades.

Produza primeiro um mapa resumido da arquitetura atual e das funcionalidades que precisam ser expostas pela API.

Não comece alterando arquivos antes de entender o fluxo atual.

2. Não reescreva as regras de negócio sem necessidade

O projeto já possui regras de negócio e autorização implementadas.

Preserve essas regras sempre que possível.

Em especial, procure reaproveitar as regras existentes nos models/managers, como:

pode_editar;
pode_excluir;
para_usuario;
regras de proprietário;
regras de colaboradores;
regras de grupos.

Não duplique essas regras em vários endpoints.

Se uma regra atualmente estiver implementada apenas dentro de uma view, avalie se ela deveria ser extraída para uma camada reutilizável antes de ser utilizada pela API.

3. Criar uma camada de API

Crie uma estrutura organizada para a API.

Não coloque toda a API em um único arquivo.

A estrutura deve permitir crescimento futuro.

Pode utilizar Django REST Framework se considerar tecnicamente adequado. Caso escolha utilizá-lo, explique brevemente por que ele é apropriado para este projeto e faça a integração de forma consistente.

Organize os endpoints por domínio/funcionalidade, por exemplo:

autenticação;
usuários;
ToDos;
pastas;
colaboração;
grupos;
checklist;
agenda;
arquivos/imagens.

Os nomes exatos devem ser definidos depois da análise do projeto atual.

4. Endpoints

Mapeie as funcionalidades existentes para endpoints HTTP.

Por exemplo:

GET /api/todos/
GET /api/todos/{id}/
POST /api/todos/
PATCH /api/todos/{id}/
DELETE /api/todos/{id}/

Mas não limite a API a esses exemplos.

Crie endpoints para todas as funcionalidades necessárias do sistema atual.

A API deve contemplar, quando aplicável:

criação;
leitura;
atualização;
exclusão;
filtros;
pesquisa;
paginação, se fizer sentido;
relacionamentos;
uploads;
colaboração;
permissões;
checklist;
agenda.
5. Autenticação

Troque o que existe hoje por JWT

6. Segurança

Não enfraqueça as proteções existentes.

Preste atenção especialmente a:

autenticação;
autorização;
CSRF;
CORS;
cookies;
SameSite;
Secure;
uploads;
acesso a imagens/arquivos;
exposição de dados de outros usuários.

Um usuário não pode acessar ou modificar dados de outro usuário simplesmente alterando um ID na URL.

Exemplo:

GET /api/todos/15/

deve verificar se o usuário autenticado pode visualizar o Todo 15.

O mesmo deve ocorrer para:

edição;
exclusão;
pastas;
colaboração;
grupos;
checklist;
agenda;
arquivos.
7. Respostas JSON

Defina uma estrutura consistente para as respostas.

Por exemplo:

Sucesso:

{
"id": 1,
"title": "Estudar Go",
...
}

Erro:

{
"detail": "Você não possui permissão para realizar esta ação."
}

Use códigos HTTP apropriados:

200;
201;
204;
400;
401;
403;
404;
409, quando aplicável;
500 somente para erros inesperados.

Não retorne HTML pelos endpoints da API.

8. Validação

A validação que atualmente ocorre nos Django Forms não deve continuar existindo na API deve ser trocada pela serialização.

Não confie na validação feita pelo frontend.

A API deve validar:

campos obrigatórios;
formatos;
relacionamentos;
permissões;
regras específicas do domínio.

Evite duplicar a mesma validação em vários lugares.

9. Compatibilidade com o sistema atual

Não se preocupe com compatibiladade com templates, vai existir uma separação completa, portanto este repositorio será destinada apenas a API, a interface será retirada. Observe que não precisa apagar o que existe, monte a API em paralelo ao sistema atual.

10. Testes

Crie testes para os endpoints mais importantes (deixe esta etapa por ultimo).

Principalmente:

autenticação;
criação de Todo;
edição;
exclusão;
acesso não autorizado;
colaboração;
pastas;
checklist;
agenda.

Inclua testes para garantir que um usuário não consiga acessar dados de outro usuário.

Não considere a API pronta simplesmente porque os endpoints respondem 200.

11. Documentação

Documente a API.

Idealmente, utilize OpenAPI/Swagger se a tecnologia escolhida permitir isso de maneira simples.

A documentação deve deixar claro:

endpoint;
método HTTP;
parâmetros;
corpo da requisição;
resposta;
erros;
autenticação necessária.

Também atualize a documentação arquitetural do projeto explicando a nova estrutura.

12. Banco de dados

Altere o banco de dados

Migre para PostgreSQL (iremos usar docker, mas você não precisa implementar isso agora)

A mudança de banco pode ser tratada como uma etapa separada.

13. Deploy

Nesta etapa, prepare o backend para funcionar como API em produção, mas não faça mudanças de hospedagem desnecessárias.

Deixe claro quais configurações serão necessárias futuramente para:

domínio da API;
CORS;
cookies;
HTTPS;
arquivos estáticos;
media/uploads;
variáveis de ambiente.
14. Forma de execução

Não tente fazer toda a transformação de uma vez.

Trabalhe em etapas:

Etapa 1

Analisar o projeto e produzir o mapa de funcionalidades.

Etapa 2

Estruturar a API.

Etapa 3

Implementar autenticação.

Etapa 4

Implementar ToDos e pastas.

Etapa 5

Implementar colaboração e grupos.

Etapa 6

Implementar checklist.

Etapa 7

Implementar agenda.

Etapa 8

Implementar arquivos/imagens.

Etapa 9

Testar permissões e fluxos completos.

Etapa 10

Documentar a API.

Depois de cada etapa, execute os testes e verifique se o sistema antigo continua funcionando.

15. Regra importante

Não faça uma "reescrita por preferência".

O objetivo não é modernizar tudo ao mesmo tempo.

Não altere sem necessidade (salvo em casos de erros grosseiros):

models;
regras de negócio;
estrutura do banco;
funcionalidades;
comportamento do sistema.

A prioridade é:

separar a API do frontend mantendo o funcionamento existente.

Se encontrar uma parte do código que precise ser refatorada para permitir uma API adequada, faça a refatoração somente quando houver uma justificativa técnica clara e documente a alteração.

Resultado esperado

Ao final desta tarefa, quero ter:

Um backend Django capaz de funcionar como API.
Endpoints cobrindo as funcionalidades atuais.
Autenticação funcionando.
Autorização funcionando.
Respostas JSON consistentes.
Uploads funcionando pela API.
Testes para os principais fluxos.
Documentação dos endpoints.
O frontend atual não possuir compatibilidade com a API, mas ainda funcionando com arquitetura antiga
Uma arquitetura preparada para que posteriormente integrar com qualquer cliente http/https

Antes de finalizar, apresente:

quais arquivos foram criados;
quais arquivos foram modificados;
quais endpoints foram criados;
quais funcionalidades ainda não foram migradas;
quais decisões arquiteturais foram tomadas;
quais problemas ou riscos foram encontrados;
como executar e testar a API localmente.

Não considere a tarefa concluída apenas porque a API inicia. Ela deve ser capaz de reproduzir as funcionalidades relevantes do sistema atual com as mesmas regras de acesso.