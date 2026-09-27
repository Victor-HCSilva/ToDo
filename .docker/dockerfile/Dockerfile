FROM python:3.12-slim

# Evita que o Python escreva arquivos .pyc e força o stdout sem buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# Instala dependências do sistema necessárias para compilar libs (ex: psycopg2) e utilitários
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o script de inicialização e dá permissão de execução
COPY .docker/scripts/environment.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copia o código da aplicação
COPY ./src /app/src

# O diretório de trabalho padrão será a raiz do código Django
WORKDIR /app/src

ENTRYPOINT ["/entrypoint.sh"]