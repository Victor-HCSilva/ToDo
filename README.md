# Lista de tarefas com Django

https://victoraccount2.pythonanywhere.com/main/

## Descrição
- Lista de tarefas com Framework BackEnd `Django` e o Framework `Tailwind CSS` para FrontEnd

---

- Ilustração
![<imagem>](<docs/imgs/agenda.png>)

- Anotações com suporte a markdown
![<imagem>](<docs/imgs/markdown.png>)

- Lista de tarefas
![<imagem>](<docs/imgs/lista-de-tarefas.png>)

- Agenda
![<imagem>](<docs/imgs/agenda.png>)

- Imagens relacionadas as anotações
![<imagem>](<docs/imgs/anotacao-image.png>)


---
- 🆙🆙🆙 Fique à vontade para fazer um `fork`.

### Instalação (Requer `Python`🐍 e `Git` 🧑‍💻 Instalados):

### Linux

- Clone o repositório:
```bash
git clone <este repositorio>
```
- Crie um ambiente virtual:
```bash
python3.12.3 -m venv .venv
```
- Ative seu ambiente virtual:
```bash
source .venv/bin/activate
```
- Instale as bibliotecas:
```bash
# ToDo — Lista de Tarefas (Django monolito)

Resumo rápido
- Pequeno monolito Django com 3 apps principais: `main` (anotações/tarefas), `agenda` (calendário/eventos) e `checklist` (tarefas e itens). Frontend usa Bulma CSS e templates Django.

Objetivo deste repositório
- Congelar estado atual para pausa de desenvolvimento: documentação mínima, pequenas correções de higiene e backlog organizado.

Rápido "Getting started" (Linux)
```bash
git clone <este-repositorio>
cd ToDo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/manage.py migrate
python src/manage.py runserver
```

Dependências
- Veja `requirements.txt` para a lista completa. Projeto foi testado com Python 3.12 + Django 5.x (veja versão no `src/.venv` se houver dúvidas).

Variáveis de ambiente
- O projeto carrega `.envs/.env` (pré-configurado no `src/core/settings.py`). As variáveis importantes:
	- `SECRET_KEY` — chave do Django (obrigatório)
	- `DEBUG` — `True`/`False`
	- `TRUSTED_HOSTS` — hosts confiáveis, separados por vírgula

Estrutura e comandos úteis
- Código está em `src/` (manage.py em `src/manage.py`).
- Comandos úteis:
	- `python src/manage.py createsuperuser`
	- `python src/manage.py loaddata <fixture>` (caso tenha fixtures)

Congelamento (freeze) — nota para manutenção
- Para pausar o projeto mantenha o repositório com tags (ex: `v1.0-freeze`) e salve um snapshot da `.envs/.env` seguro fora do repositório.
- Não há mudanças de arquitetura neste commit — apenas documentação e pequenas remoções de prints de debug.

Onde ler mais
- Veja `docs/ARCHITECTURE.md` e `docs/TECHNICAL.md` para informações sobre arquitetura e detalhes técnicos.

Se quiser que eu execute testes, gere uma tag ou adicione um arquivo de checklist para retomada, diga qual ação prefere em seguida.

