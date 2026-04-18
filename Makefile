# Makefile para gerenciar a aplicação anotacoes com Docker Compose

# Rodar a aplicação (build + start)

migrate:
	@echo "Executando migrações"
	@src/python3 manage.py makemigrations
	@src/python3 manage.py migrate
	@clear

save_all:
	@git add .
	@git commit
