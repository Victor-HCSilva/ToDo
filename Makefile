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

dev:
	python src/manage.py makemigrations
	python src/manage.py migrate
	python src/manage.py runserver

# Instala as dependências
install: venv
	@echo "Instalando dependências..."
	$(PIP) install -r requirements.txt

# Inicia o servidor de desenvolvimento
runserver:
	@echo "Iniciando servidor de desenvolvimento..."
	$(VENV_DIR)/bin/$(PYTHON) $(MANAGE) runserver

