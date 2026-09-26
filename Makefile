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
	#python3 -m venv .venv 
	#activate
	#@$(PIP) install -r requirements.txt
	python3 src/manage.py makemigrations
	python3 src/manage.py migrate
	python3 src/manage.py runserver 4441

# Instala as dependências
install: venv
	@echo "Instalando dependências..."
	$(PIP) install -r requirements.txt

# Inicia o servidor de desenvolvimento
runserver:
	@echo "Iniciando servidor de desenvolvimento..."
	$(VENV_DIR)/bin/$(PYTHON) $(MANAGE) runserver

