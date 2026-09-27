#!/bin/sh
set -e

echo "Aguardando o PostgreSQL inicializar..."
while ! nc -z "${DB_HOST:-db}" "${DB_PORT:-5432}"; do
  sleep 0.5
done
echo "PostgreSQL conectado com sucesso!"

echo "Aguardando o Redis inicializar..."
while ! nc -z "${REDIS_HOST:-redis}" "${REDIS_PORT:-6379}"; do
  sleep 0.5
done
echo "Redis conectado com sucesso!"

# Executa migrações apenas se for o container da API (evita condição de corrida no worker/beat)
if [ "$1" = "python" ] && [ "$2" = "manage.py" ] && [ "$3" = "runserver" ]; then
    echo "Aplicando migrações do banco de dados..."
    python manage.py migrate --noinput
fi

exec "$@"