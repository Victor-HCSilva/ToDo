# Variáveis
PYTHON = python
MANAGE = src/manage.py
VENV_DIR = .venv
PIP = $(VENV_DIR)/bin/pip

# Para Windows, use:
# PYTHON = python
# MANAGE = src\manage.py
# VENV_DIR = .venv
# PIP = $(VENV_DIR)\Scripts\pip.exe

.PHONY: help install venv activate runserver makemigrations migrate createsuperuser test collectstatic lint clean

# Regra padrão: exibe ajuda se nenhum comando for especificado
help:
	@echo "Comandos Django comuns para o projeto:"
	@echo ""
	@echo "  make help             - Exibe esta mensagem de ajuda."
	@echo "  make install          - Instala as dependências (cria venv se não existir)."
	@echo "  make venv             - Cria o amb'iente virtual."
	@echo "  make activate         - Ativa o ambiente virtual (para uso manual)."
	@echo "  make runserver        - Inicia o servidor de desenvolvimento Django."
	@echo "  make makemigrations   - Cria novas migrações."
	@echo "  make migrate          - Aplica as migrações ao banco de dados."
	@echo "  make createsuperuser  - Cria um superusuário Django."
	@echo "  make test             - Executa os testes do projeto."
	@echo "  make collectstatic    - Coleta arquivos estáticos."
	@echo "  make lint             - Executa um linter (ex: flake8, black)."
	@echo "  make clean            - Remove arquivos temporários e o ambiente virtual."

# Cria o ambiente virtual
venv:
	@echo "Criando ambiente virtual..."
	$(PYTHON) -m venv $(VENV_DIR)

# Ativa o ambiente virtual (para uso manual, não para ser usado diretamente dentro do make)
activate:
	@echo "Para ativar o ambiente virtual manualmente, use:"
	@echo "source $(VENV_DIR)/bin/activate (Linux/macOS)"
	@echo "$(VENV_DIR)\\Scripts\\activate (Windows)"

# Instala as dependências
install: venv
	@echo "Instalando dependências..."
	$(PIP) install -r requirements.txt

# Inicia o servidor de desenvolvimento
runserver:
	@echo "Iniciando servidor de desenvolvimento..."
	$(VENV_DIR)/bin/$(PYTHON) $(MANAGE) runserver

# Cria as migrações
makemigrations:
	@echo "Criando migrações..."
	$(VENV_DIR)/bin/$(PYTHON) $(MANAGE) makemigrations

# Aplica as migrações
migrate:
	@echo "Aplicando migrações..."
	$(VENV_DIR)/bin/$(PYTHON) $(MANAGE) migrate

# Cria um superusuário
createsuperuser:
	@echo "Criando superusuário..."
	$(VENV_DIR)/bin/$(PYTHON) $(MANAGE) createsuperuser

# Executa os testes
test:
	@echo "Executando testes..."
	$(VENV_DIR)/bin/$(PYTHON) $(MANAGE) test

# Coleta arquivos estáticos
collectstatic:
	@echo "Coletando arquivos estáticos..."
	$(VENV_DIR)/bin/$(PYTHON) $(MANAGE) collectstatic --noinput

# Executa um linter (ex: flake8) - Exemplo
lint:
	@echo "Executando linter (Flake8)..."
	$(VENV_DIR)/bin/flake8 src/

# Limpa arquivos temporários e o ambiente virtual
clean:
	@echo "Limpando arquivos temporários e ambiente virtual..."
	rm -rf $(VENV_DIR)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".mypy_cache" -delete