#!/bin/sh

# Extrai host e porta do DATABASE_URL
DATABASE_URL=${DATABASE_URL:-""}
if [ -z "$DATABASE_URL" ]; then
    echo "DATABASE_URL não definida."
    exit 1
fi

# Extrai o host e a porta corretamente
POSTGRES_HOST=$(echo $DATABASE_URL | sed -E 's|.*://([^:/]+).*|\1|')   # Extrai apenas o host
POSTGRES_PORT=$(echo $DATABASE_URL | sed -E 's|.*:([0-9]+).*|\1|')    # Extrai apenas a porta

# Exibe os valores para debug
echo "Host do PostgreSQL: $POSTGRES_HOST"
echo "Porta do PostgreSQL: $POSTGRES_PORT"

# Aguarda até que o serviço do PostgreSQL esteja disponível
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "Aguardando inicialização do banco de dados PostgreSQL ($POSTGRES_HOST:$POSTGRES_PORT)..."
    sleep 2
done

echo "Banco de dados PostgreSQL iniciado com sucesso ($POSTGRES_HOST:$POSTGRES_PORT)"